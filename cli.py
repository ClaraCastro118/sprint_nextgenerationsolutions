"""Uso:  python -m nextgen.cli --briefing src/data/briefing_exemplo.json --mock bom
        python -m nextgen.cli --briefing ... --mock ruim     (demonstra o bloqueio)
        python -m nextgen.cli --briefing ...                 (usa o modelo real; exige .env)
"""
import argparse
import json
import sys
from pathlib import Path

from .config import forbidden_terms_from_env, load_env
from .generator import GenerationError, gerar
from .llm import AnthropicLLM, LLMError, MockLLM
from .manual import load_manual
from .models import Briefing, BriefingError

DATA = Path(__file__).resolve().parent.parent / "data"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="nextgen")
    ap.add_argument("--briefing", required=True, help="JSON do briefing")
    ap.add_argument("--manual", default=str(DATA / "manual_marca_sintetico.json"))
    ap.add_argument("--mock", choices=["bom", "ruim"], help="usa saída simulada (sem API)")
    ap.add_argument("--json", action="store_true", help="imprime o resultado em JSON")
    args = ap.parse_args(argv)

    load_env()
    manual = load_manual(args.manual)
    try:
        briefing = Briefing.from_dict(json.loads(Path(args.briefing).read_text(encoding="utf-8")),
                                      manual.formatos_validos)
    except BriefingError as e:
        print("Briefing inválido:", *[f"  - {p}" for p in e.problems], sep="\n", file=sys.stderr)
        return 2

    try:
        llm = MockLLM(args.mock) if args.mock else AnthropicLLM()
        res = gerar(briefing, manual, llm, forbidden_terms_from_env())
    except (LLMError, GenerationError) as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(res.to_dict(), ensure_ascii=False, indent=2))
        return 0
    print(f"Manual v{manual.versao} | tempo: {res.tempo_segundos}s | tentativas: {res.tentativas_geracao}\n")
    for p in res.pecas:
        v = p.variacao
        print(f"[{v.formato}] status: {p.status.upper()}")
        print(f"  título: {v.titulo}\n  texto : {v.texto}\n  cta   : {v.cta}")
        for r in p.conformidade.resultados:
            print(f"   {'OK ' if r.passou else 'FALHA'} {r.regra_id} {r.descricao}" + (f" — {r.motivo}" if r.motivo else ""))
        print()
    print("Nenhuma peça é aprovada automaticamente: as conformes aguardam revisão humana.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
