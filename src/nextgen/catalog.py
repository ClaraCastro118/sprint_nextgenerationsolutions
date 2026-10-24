"""Catálogo de produtos (sintético) — fonte única de verdade para dados comerciais.

Ponto de substituição documentado: trocar `load_catalog()` por um adaptador de
PIM/ERP real mantendo a interface `Catalog.get(id) -> Product | None`.
"""
import json
from pathlib import Path

from .models import Product


class Catalog:
    def __init__(self, produtos: list[Product], atualizado_em: str, origem: str):
        self._por_id = {p.id: p for p in produtos}
        self.atualizado_em = atualizado_em
        self.origem = origem

    def get(self, produto_id: str | None) -> Product | None:
        if not produto_id:
            return None
        return self._por_id.get(produto_id)

    def todos(self) -> list[Product]:
        return list(self._por_id.values())


def load_catalog(path: str | Path) -> Catalog:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    produtos = [Product(**p) for p in data["produtos"]]
    return Catalog(produtos=produtos, atualizado_em=data["atualizado_em"],
                   origem=data.get("_aviso", "catalogo_sintetico_demo_v1"))