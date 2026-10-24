import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from nextgen import approval, governance, templates
from nextgen.catalog import load_catalog
from nextgen.generator import gerar
from nextgen.llm import MockLLM
from nextgen.manual import load_manual
from nextgen.metrics import estimar_ganho
from nextgen.models import (Briefing, STATUS_APROVADA, STATUS_BLOQUEADA,
                            STATUS_EM_REVISAO, Variation)

MANUAL = load_manual(ROOT / "src/data/manual_marca_sintetico.json")
CATALOG = load_catalog(ROOT / "src/data/products_demo.json")
EX = json.loads((ROOT / "src/data/briefing_exemplo.json").read_text(encoding="utf-8"))
EX_BLOQ = json.loads((ROOT / "src/data/briefing_bloqueado.json").read_text(encoding="utf-8"))

class MockSemDisclaimer(MockLLM):
    """Simula uma IA que esqueceu o aviso da ANVISA."""
    def complete(self, system: str, user: str) -> str:
        if "TAREFA: GERAR" in user:
            return json.dumps({"variacoes": [{"formato": "feed_social", "titulo": "Remedio", "texto": "Texto sem aviso legal.", "cta": "Compre"}]})
        return json.dumps({"aprovado": True, "motivo": "ok"})

def briefing(**over):
    return Briefing.from_dict({**EX, **over}, MANUAL.formatos_validos)

class TestCatalogo(unittest.TestCase):
    def test_quatro_produtos_sinteticos(self):
        self.assertEqual(len(CATALOG.todos()), 4)
        self.assertEqual(CATALOG.get("SKU-EX-001").preco_exibicao(), 39.90)

    def test_oferta_vencida_detectada(self):
        self.assertFalse(CATALOG.get("SKU-EX-003").oferta_valida_em())
        self.assertTrue(CATALOG.get("SKU-EX-001").oferta_valida_em())

    def test_produto_inexistente(self):
        self.assertIsNone(CATALOG.get("SKU-NAO-EXISTE"))

class TestGovernancaComercial(unittest.TestCase):
    def _v(self, **over):
        base = dict(formato="feed_social", titulo="t", texto="t", cta="c")
        base.update(over)
        return Variation(**base)

    def test_produto_inexistente_bloqueia(self):
        r = governance.verificar_produto(self._v(produto_id="X"), None, MANUAL)
        self.assertFalse(r.passou)

    def test_preco_divergente_bloqueia(self):
        v = self._v(texto="De R$ 19,90 por R$ 39,90", preco_formatado="R$ 19,90")
        r = governance.verificar_preco(v, CATALOG.get("SKU-EX-001"), MANUAL)
        self.assertFalse(r.passou)

    def test_preco_ausente_no_texto_passa(self):
        v = self._v(preco_formatado="R$ 39,90")
        r = governance.verificar_preco(v, CATALOG.get("SKU-EX-001"), MANUAL)
        self.assertTrue(r.passou)

    def test_oferta_vencida_bloqueia(self):
        r = governance.verificar_validade(self._v(), CATALOG.get("SKU-EX-003"), MANUAL)
        self.assertFalse(r.passou)

    def test_canal_nao_permitido_bloqueia(self):
        v = self._v(formato="banner_web")
        r = governance.verificar_canais(v, CATALOG.get("SKU-EX-003"), MANUAL)
        self.assertFalse(r.passou)

class TestFluxoComercial(unittest.TestCase):
    def test_caso_valido_gera_tres_formatos_e_revisao(self):
        b = briefing(formatos=["feed_social", "story", "banner_web"])
        res = gerar(b, MANUAL, MockLLM("bom"), catalog=CATALOG)
        self.assertEqual(len(res.pecas), 3)
        for p in res.pecas:
            self.assertEqual(p.status, STATUS_EM_REVISAO)
            self.assertEqual(p.variacao.produto_id, "SKU-EX-001")
            self.assertTrue(p.variacao.preco_formatado)

    def test_caso_bloqueado_por_validade(self):
        b = Briefing.from_dict(EX_BLOQ, MANUAL.formatos_validos)
        res = gerar(b, MANUAL, MockLLM("bom"), catalog=CATALOG)
        for p in res.pecas:
            self.assertEqual(p.status, STATUS_BLOQUEADA)
            falhas = {r.regra_id for r in p.conformidade.resultados if not r.passou}
            self.assertIn("G-08", falhas)

    def test_medicamento_sem_disclaimer_bloqueia(self):
        ex = json.loads((ROOT / "src/data/briefing_medicamento.json").read_text())
        b = Briefing.from_dict(ex, MANUAL.formatos_validos)
        # Usa o mock que esquece o disclaimer de propósito
        res = gerar(b, MANUAL, MockSemDisclaimer(), catalog=CATALOG)
        for p in res.pecas:
            self.assertEqual(p.status, STATUS_BLOQUEADA)
            falhas = {r.regra_id for r in p.conformidade.resultados if not r.passou}
            self.assertIn("G-10", falhas)

class TestTemplates(unittest.TestCase):
    def test_tres_formatos_renderizam(self):
        b = briefing(formatos=["feed_social", "story", "banner_web"])
        res = gerar(b, MANUAL, MockLLM("bom"), catalog=CATALOG)
        for p in res.pecas:
            product = CATALOG.get(p.variacao.produto_id)
            html = templates.render_peca(p, product, MANUAL, variante=1)
            self.assertIn("<!DOCTYPE html>", html)
            self.assertIn(p.variacao.titulo, html)
            if product.preco_exibicao():
                self.assertIn("R$", html)

    def test_html_escapa_conteudo(self):
        b = briefing(formatos=["feed_social"])
        res = gerar(b, MANUAL, MockLLM("bom"), catalog=CATALOG)
        p = res.pecas[0]
        p.variacao.titulo = "<script>alert(1)</script>"
        html = templates.render_peca(p, None, MANUAL)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_variantes_visuais_diferentes(self):
        b = briefing(formatos=["feed_social"])
        res = gerar(b, MANUAL, MockLLM("bom"), catalog=CATALOG)
        p = res.pecas[0]
        h1 = templates.render_peca(p, None, MANUAL, variante=1)
        h2 = templates.render_peca(p, None, MANUAL, variante=2)
        self.assertNotEqual(h1, h2)

class TestAprovacao(unittest.TestCase):
    def _bloqueada_e_aprovada(self):
        b = Briefing.from_dict(EX_BLOQ, MANUAL.formatos_validos)
        bloq = gerar(b, MANUAL, MockLLM("bom"), catalog=CATALOG).pecas[0]
        ok = gerar(briefing(), MANUAL, MockLLM("bom"), catalog=CATALOG).pecas[0]
        return bloq, ok

    def test_bloqueada_nao_pode_ser_aprovada(self):
        bloq, _ = self._bloqueada_e_aprovada()
        ok, motivo = approval.pode_aprovar(bloq)
        self.assertFalse(ok)
        self.assertIn("bloqueada", motivo.lower())

    def test_conforme_aprova_e_registra(self):
        _, p = self._bloqueada_e_aprovada()
        ok, _ = approval.aprovar(p, "revisor-x")
        self.assertTrue(ok)
        self.assertEqual(p.status, STATUS_APROVADA)
        self.assertEqual(p.decisao["responsavel"], "revisor-x")

    def test_rejeicao_exige_comentario(self):
        _, p = self._bloqueada_e_aprovada()
        ok, msg = approval.rejeitar(p, "revisor-x", "")
        self.assertFalse(ok)
        self.assertIn("comentário", msg)

class TestMetricas(unittest.TestCase):
    def test_reducao_calculada(self):
        r = estimar_ganho(20.0, 3, 30.0)
        self.assertGreater(r["reducao_pct"], 99)
        self.assertAlmostEqual(r["tempo_manual_total_min"], 60.0)

    def test_zero_invalido(self):
        self.assertIn("erro", estimar_ganho(0, 3, 30.0))
        self.assertIn("erro", estimar_ganho(20.0, 0, 30.0))

if __name__ == "__main__":
    unittest.main(verbosity=2)