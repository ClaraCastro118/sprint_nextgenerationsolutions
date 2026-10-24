"""Transições de estado de aprovação humana.

Regra: peça bloqueada ou não conforme **não pode** ser aprovada, por qualquer caminho.
"""

from datetime import datetime, timezone

from .models import (PieceResult, STATUS_APROVADA, STATUS_BLOQUEADA,
                     STATUS_EM_REVISAO, STATUS_REPROVADA)
import json
from pathlib import Path
LOG_FILE = Path("audit_log.jsonl")

def _registrar_log(peca, acao, responsavel, comentario):
    log_entry = {
        "timestamp": _agora_iso(), "formato": peca.variacao.formato,
        "titulo": peca.variacao.titulo, "acao": acao,
        "responsavel": responsavel, "comentario": comentario
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

ROTULOS = {
    STATUS_EM_REVISAO: "Aguardando revisão humana",
    STATUS_BLOQUEADA: "Bloqueada pela governança",
    STATUS_APROVADA: "Aprovada por humano",
    STATUS_REPROVADA: "Reprovada por humano",
}


def pode_aprovar(peca: PieceResult) -> tuple[bool, str]:
    if peca.status == STATUS_BLOQUEADA:
        return False, "Peça bloqueada pela governança: corrija os problemas antes de aprovar."
    if not peca.conformidade.conforme:
        return False, "Existem falhas de conformidade não resolvidas."
    if peca.status == STATUS_APROVADA:
        return False, "Peça já está aprovada."
    return True, ""


def pode_rejeitar(peca: PieceResult) -> tuple[bool, str]:
    if peca.status == STATUS_APROVADA:
        return False, "Peça já aprovada; reabertura exige nova rodada de revisão."
    return True, ""


def _agora_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def aprovar(peca: PieceResult, responsavel: str, comentario: str = "") -> tuple[bool, str]:
    ok, motivo = pode_aprovar(peca)
    if not ok:
        return False, motivo
    peca.status = STATUS_APROVADA
    peca.decisao = {"acao": "aprovada", "responsavel": responsavel or "revisor",
                    "em": _agora_iso(), "comentario": comentario}
    _registrar_log(peca, "aprovada", responsavel, comentario)
    return True, "Peça aprovada."


def rejeitar(peca: PieceResult, responsavel: str, comentario: str) -> tuple[bool, str]:
    ok, motivo = pode_rejeitar(peca)
    if not ok:
        return False, motivo
    if not comentario.strip():
        return False, "Rejeição exige comentário."
    peca.status = STATUS_REPROVADA
    peca.decisao = {"acao": "reprovada", "responsavel": responsavel or "revisor",
                    "em": _agora_iso(), "comentario": comentario.strip()}
    return True, "Peça reprovada."