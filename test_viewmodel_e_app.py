"""Testes da lógica da tela e um teste de fumaça do app.py com um Streamlit FALSO.

Importante: o teste de fumaça só garante que o fluxo do app.py roda sem erros internos e usa
apenas as funções listadas em FUNCOES_STREAMLIT_USADAS. Ele NÃO substitui rodar o app com o
Streamlit de verdade (streamlit run src/app.py).
"""
import contextlib
import json
import runpy
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from nextgen import viewmodel as vm  # noqa: E402
from nextgen.generator import gerar  # noqa: E402
from nextgen.llm import LLMError, MockLLM  # noqa: E402
from nextgen.manual import load_manual  # noqa: E402

MANUAL = load_manual(ROOT / "src/data/manual_marca_sintetico.json")
EX = json.loads((ROOT / "src/data/briefing_exemplo.json").read_text(encoding="utf-8"))


class TestViewModel(unittest.TestCase):
    def test_montar_briefing_valido_e_invalido(self):
        b, p = vm.montar_briefing(EX, MANUAL)
        self.assertIsNotNone(b)
        self.assertEqual(p, [])
        b, p = vm.montar_briefing({**EX, "objetivo": "", "formatos": []}, MANUAL)
        self.assertIsNone(b)
        self.assertGreaterEqual(len(p), 2)

    def test_resumo_e_tabelas(self):
        b, _ = vm.montar_briefing(EX, MANUAL)
        res = gerar(b, MANUAL, MockLLM("ruim"))
        r = vm.resumo(res)
        self.assertEqual((r["total"], r["bloqueadas"], r["em_revisao"]), (2, 2, 0))
        self.assertTrue(any(l["Resultado"] == "FALHOU" for l in vm.linhas_regras(res.pecas[0])))
        self.assertTrue(any(c["Dentro do limite"] == "NÃO" for c in vm.contadores(res.pecas[0], MANUAL)))

    def test_modo_real_sem_configuracao_da_erro_claro(self):
        import os
        for k in ("AI_API_KEY", "AI_MODEL"):
            os.environ.pop(k, None)
        with self.assertRaises(LLMError):
            vm.criar_llm(vm.MODO_REAL)


FUNCOES_STREAMLIT_USADAS = {
    "set_page_config", "title", "write", "markdown", "caption", "subheader", "info", "error",
    "text_area", "text_input", "multiselect", "form", "form_submit_button", "spinner",
    "columns", "metric", "table", "expander", "sidebar", "session_state",
}


class _Ctx:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def metric(self, *a, **k): pass


class FakeStreamlit(types.ModuleType):
    def __init__(self, modo, submit):
        super().__init__("streamlit")
        self.session_state = {}
        self._modo, self._submit = modo, submit
        self.chamadas = []

        class Side:
            def __getattr__(s, name):
                if name == "radio":
                    return lambda label, options, **k: self._modo
                if name not in FUNCOES_STREAMLIT_USADAS:
                    raise AttributeError(f"sidebar.{name} não está na lista de funções previstas")
                return lambda *a, **k: self.chamadas.append(("sidebar." + name, a))
        self.sidebar = Side()

    def __getattr__(self, name):
        if name.startswith("__") or name not in FUNCOES_STREAMLIT_USADAS:
            raise AttributeError(f"st.{name} não está na lista de funções previstas")
        def f(*a, **k):
            self.chamadas.append((name, a))
            if name == "text_area":
                return k.get("value", "")
            if name == "text_input":
                return k.get("value", "")
            if name == "multiselect":
                return k.get("default", [])
            if name == "form_submit_button":
                return self._submit
            if name == "columns":
                n = a[0]
                return [_Ctx() for _ in range(n)]
            if name in ("form", "spinner", "expander"):
                return _Ctx()
            return None
        return f


class TestAppFumaca(unittest.TestCase):
    def rodar(self, modo, submit=True):
        fake = FakeStreamlit(modo, submit)
        antigo = sys.modules.get("streamlit")
        sys.modules["streamlit"] = fake
        try:
            runpy.run_path(str(ROOT / "src/app.py"), run_name="__main__")
        finally:
            if antigo is None:
                sys.modules.pop("streamlit", None)
            else:
                sys.modules["streamlit"] = antigo
        return fake

    def test_fluxo_com_pecas_conformes(self):
        fake = self.rodar(vm.MODO_SIM_BOM)
        self.assertIsNotNone(fake.session_state["resultado"])
        nomes = [c[0] for c in fake.chamadas]
        self.assertIn("table", nomes)
        self.assertNotIn("button", nomes)  # sem botão de aprovar

    def test_fluxo_com_pecas_bloqueadas(self):
        fake = self.rodar(vm.MODO_SIM_RUIM)
        self.assertTrue(all(p.status == "bloqueada" for p in fake.session_state["resultado"].pecas))

    def test_modo_real_sem_chave_mostra_erro_e_nao_quebra(self):
        import os
        for k in ("AI_API_KEY", "AI_MODEL"):
            os.environ.pop(k, None)
        fake = self.rodar(vm.MODO_REAL)
        self.assertIsNone(fake.session_state["resultado"])
        self.assertIn("error", [c[0] for c in fake.chamadas])

    def test_sem_envio_nao_gera_nada(self):
        fake = self.rodar(vm.MODO_SIM_BOM, submit=False)
        self.assertNotIn("resultado", fake.session_state)


if __name__ == "__main__":
    unittest.main(verbosity=2)
