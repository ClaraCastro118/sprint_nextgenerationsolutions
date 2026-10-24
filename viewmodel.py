"""Lógica de apresentação da interface, separada do Streamlit para poder ser testada sem ele."""
from .llm import AnthropicLLM, MockLLM
from .manual import Manual
from .models import (Briefing, BriefingError, GenerationResult, PieceResult,
                     STATUS_BLOQUEADA, STATUS_EM_REVISAO)

MODO_SIM_BOM = "Simulado — peças conformes"
MODO_SIM_RUIM = "Simulado — peças inadequadas (demonstra o bloqueio)"
MODO_REAL = "Modelo de IA real (exige .env)"
MODOS = [MODO_SIM_BOM, MODO_SIM_RUIM, MODO_REAL]

ROTULO_STATUS = {
    STATUS_EM_REVISAO: "Aguardando revisão humana",
    STATUS_BLOQUEADA: "Bloqueada pela governança",
}


def criar_llm(modo: str):
    """Levanta LLMError (modo real sem configuração) — a tela trata e explica."""
    if modo == MODO_SIM_BOM:
        return MockLLM("bom")
    if modo == MODO_SIM_RUIM:
        return MockLLM("ruim")
    return AnthropicLLM()


def montar_briefing(valores: dict, manual: Manual) -> tuple[Briefing | None, list[str]]:
    try:
        return Briefing.from_dict(valores, manual.formatos_validos), []
    except BriefingError as e:
        return None, e.problems


def contadores(peca: PieceResult, manual: Manual) -> list[dict]:
    v = peca.variacao
    limites = manual.formatos[v.formato]["limites"]
    return [
        {"Campo": campo, "Uso": f"{len(getattr(v, campo))}/{limite}",
         "Dentro do limite": "sim" if len(getattr(v, campo)) <= limite else "NÃO"}
        for campo, limite in limites.items()
    ]


def linhas_regras(peca: PieceResult) -> list[dict]:
    return [
        {"Regra": r.regra_id, "Descrição": r.descricao,
         "Resultado": "OK" if r.passou else "FALHOU", "Detalhe": r.motivo}
        for r in peca.conformidade.resultados
    ]


def resumo(res: GenerationResult) -> dict:
    return {
        "total": len(res.pecas),
        "em_revisao": sum(p.status == STATUS_EM_REVISAO for p in res.pecas),
        "bloqueadas": sum(p.status == STATUS_BLOQUEADA for p in res.pecas),
        "tempo_segundos": res.tempo_segundos,
        "versao_manual": res.versao_manual,
    }
