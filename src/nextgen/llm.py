"""Camada de acesso ao modelo de IA."""
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
            import anthropic
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
        except Exception as e:
            raise LLMError(f"falha ao chamar o modelo: {e}") from e
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")

class MockLLM:
    """Simula o modelo. `modo`: 'bom' (peças conformes) ou 'ruim' (viola regras)."""
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
        produto_nome = re.search(r"PRODUTO_NOME: (.+)", user)
        
        # Verifica se é o remédio para injetar o disclaimer da ANVISA
        is_medicamento = "SKU-EX-004" in user or "Analgésico" in user
        disclaimer = "\nAO PERSISTIREM OS SINTOMAS, O MÉDICO DEVERÁ SER CONSULTADO." if is_medicamento else ""
        
        variacoes = []
        for f in formatos:
            if self.modo == "ruim":
                # Modo Ruim: Texto gigante para estourar limite (G-02) e termos proibidos (G-01)
                variacoes.append({
                    "formato": f,
                    "titulo": "Oferta GARANTIDO!!! imperdível agora mesmo",
                    "texto": "Compre já, resultado garantido, 100% grátis, não perca, é milagroso, cura tudo e sem risco. " * 4,
                    "cta": "CLIQUE AQUI E COMPRE AGORA MESMO",
                    "regras_aplicadas": [],
                })
            elif f == "story":
                # Story limite: 100 caracteres
                variacoes.append({"formato": f, "titulo": "Um cuidado para o seu dia",
                                  "texto": f"Simples, no seu ritmo.{disclaimer}", 
                                  "cta": "Deslize", "regras_aplicadas": ["G-01", "G-02"]})
            elif f == "banner_web":
                # Banner limite: 90 caracteres. A frase do disclaimer tem 60, então o texto base tem que ser curto.
                variacoes.append({"formato": f, "titulo": "Cuidar de você",
                                  "texto": f"Rotina simples.{disclaimer}", 
                                  "cta": "Saiba mais", "regras_aplicadas": ["G-01", "G-02"]})
            else: # feed_social
                # Feed limite: 220 caracteres
                rotulo = f" ({produto_nome.group(1)})" if produto_nome else ""
                variacoes.append({"formato": f, "titulo": "Seu dia mais leve",
                                  "texto": f"{objetivo[:100]}{rotulo}. Conte com a gente.{disclaimer}", 
                                  "cta": "Conheça", "regras_aplicadas": ["G-01", "G-02"]})
        return json.dumps({"variacoes": variacoes}, ensure_ascii=False)