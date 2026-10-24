"""Carrega o manual de marca sintético (formato estruturado) usado por geração e governança."""
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Manual:
    versao: str
    marca: str
    tom_de_voz: dict
    paleta: list[dict]
    termos_proibidos: list[str]
    limite_emojis: int
    formatos: dict          # {id: {"descricao": str, "limites": {"titulo": n, "texto": n, "cta": n}}}
    regras: list[dict]      # [{"id","descricao","tipo","verificacao"}]

    @property
    def formatos_validos(self) -> list[str]:
        return list(self.formatos.keys())

    def regra(self, verificacao: str) -> dict:
        for r in self.regras:
            if r["verificacao"] == verificacao:
                return r
        raise KeyError(f"regra com verificacao={verificacao!r} ausente no manual")


def load_manual(path: str | Path) -> Manual:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Manual(
        versao=data["versao"],
        marca=data["marca"],
        tom_de_voz=data["tom_de_voz"],
        paleta=data["paleta"],
        termos_proibidos=data["termos_proibidos"],
        limite_emojis=data["limite_emojis"],
        formatos=data["formatos"],
        regras=data["regras"],
    )
