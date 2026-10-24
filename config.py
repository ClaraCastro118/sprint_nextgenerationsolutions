"""Configuração via variáveis de ambiente / arquivo .env (sem dependências externas).

Nenhum segredo é gravado no código. O .env está no .gitignore.
"""
import os
from pathlib import Path


def load_env(path: str = ".env") -> None:
    """Carrega pares CHAVE=valor do .env sem sobrescrever variáveis já definidas."""
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def forbidden_terms_from_env() -> list[str]:
    """Termos que identificam a empresa parceira.

    Ficam APENAS no .env local (FORBIDDEN_TERMS=termo1,termo2), nunca no
    repositório, para que o próprio código não carregue o que ele proíbe.
    """
    raw = os.environ.get("FORBIDDEN_TERMS", "")
    return [t.strip() for t in raw.split(",") if t.strip()]
