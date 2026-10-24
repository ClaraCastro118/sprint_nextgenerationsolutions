"""Camada de acesso ao modelo de IA.

Interface única `complete(system, user) -> str`. Trocar de provedor = trocar o adaptador;
o restante do sistema não muda (ponto de substituição documentado).

- MockLLM: saída simulada e determinística, para demonstração offline e testes.
- AnthropicLLM: adaptador de referência (import tardio; exige `pip install anthropic`,
  AI_API_KEY e AI_MODEL no .env). A escolha do provedor é decisão da equipe (spike T-01).
"""
import json
import os
import re
from typing import Protocol


class LLM(Protocol):
    def complete(self, system: str, user: str) -> str: ...


class LLMError(RuntimeError):
    pass


class AnthropicLLM:
    def __init__(self, api_key: str | None = None, model: str | None = None, max_tokens: int = 1500):
        api_key = api_key or os.environ.get("AI_API_KEY")
        model = model or os.environ.get("AI_MODEL")
        if not api_key or not model:
            raise LLMError("Defina AI_API_KEY e AI_MODEL no .env (veja .env.example).")
        try:
            import anthropic  # import tardio: dependência opcional
        except ImportError as e:
            raise LLMError("Instale o SDK: pip install anthropic") from e
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens

    def complete(self, system: str, user: str) -> str:
        try:
            msg = self._client.messages.create(
                model=self._model,
                max_tokens=self._max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
        except Exception as e:  # falha de rede, limite, saldo etc.
            raise LLMError(f"falha ao chamar o modelo: {e}") from e
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


class MockLLM:
    """Simula o modelo. `modo`: 'bom' (peças conformes) ou 'ruim' (viola regras de propósito)."""

    def __init__(self, modo: str = "bom"):
        self.modo = modo
        self.chamadas = 0

    def complete(self, system: str, user: str) -> str:
        self.chamadas += 1
        if "TAREFA: AVALIAR_TOM" in user:
            ruim = "GARANTIDO" in user.upper() or "!!!" in user
            return json.dumps({
                "aprovado": not ruim,
                "motivo": "tom promocional agressivo" if ruim else "tom adequado ao manual",
            }, ensure_ascii=False)
        # TAREFA: GERAR
        formatos = re.findall(r"FORMATO_SOLICITADO: (\w+)", user)
        objetivo = (re.search(r"OBJETIVO: (.+)", user) or [None, "sua campanha"])[1]
        variacoes = []
        for f in formatos:
            if self.modo == "ruim":
                variacoes.append({
                    "formato": f,
                    "titulo": "Oferta GARANTIDO!!! imperdível agora mesmo " * 3,
                    "texto": "Compre já, resultado garantido, 100% grátis, não perca " * 6,
                    "cta": "CLIQUE AQUI E COMPRE AGORA MESMO",
                    "regras_aplicadas": [],
                })
            elif f == "banner_web":
                variacoes.append({"formato": f, "titulo": "Cuidar de você fica leve",
                                  "texto": "Uma rotina de cuidado simples, no seu ritmo.", "cta": "Saiba mais",
                                  "regras_aplicadas": ["G-01", "G-02", "G-03", "G-04", "G-05"]})
            else:
                variacoes.append({"formato": f, "titulo": "Seu dia mais leve começa aqui",
                                  "texto": f"{objetivo[:150]} Conte com a gente nessa jornada.",
                                  "cta": "Conheça agora",
                                  "regras_aplicadas": ["G-01", "G-02", "G-03", "G-04", "G-05"]})
        return json.dumps({"variacoes": variacoes}, ensure_ascii=False)
