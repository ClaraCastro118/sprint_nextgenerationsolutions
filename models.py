"""Modelos de dados do fluxo: briefing -> variações -> relatório de conformidade."""
from dataclasses import dataclass, field, asdict
from typing import Optional


class BriefingError(ValueError):
    """Briefing inválido (US-01): lista todos os problemas de uma vez."""

    def __init__(self, problems: list[str]):
        self.problems = problems
        super().__init__("; ".join(problems))


@dataclass
class Briefing:
    objetivo: str
    publico: str
    formatos: list[str]            # ids definidos no manual (ex.: feed_social, banner_web)
    tom: str
    produto: Optional[str] = None
    restricoes: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict, formatos_validos: list[str]) -> "Briefing":
        problems = []
        for campo in ("objetivo", "publico", "tom"):
            if not str(data.get(campo, "")).strip():
                problems.append(f"campo obrigatório vazio: {campo}")
        formatos = data.get("formatos") or []
        if not isinstance(formatos, list) or not formatos:
            problems.append("informe ao menos um formato")
        else:
            for f in formatos:
                if f not in formatos_validos:
                    problems.append(f"formato desconhecido: {f} (válidos: {', '.join(formatos_validos)})")
        if problems:
            raise BriefingError(problems)
        return cls(
            objetivo=data["objetivo"].strip(),
            publico=data["publico"].strip(),
            formatos=list(formatos),
            tom=data["tom"].strip(),
            produto=(data.get("produto") or None),
            restricoes=(data.get("restricoes") or None),
        )


@dataclass
class Variation:
    formato: str
    titulo: str
    texto: str
    cta: str
    regras_aplicadas: list[str] = field(default_factory=list)


@dataclass
class RuleResult:
    regra_id: str
    descricao: str
    passou: bool
    motivo: str = ""


@dataclass
class ConformityReport:
    formato: str
    resultados: list[RuleResult]

    @property
    def conforme(self) -> bool:
        return all(r.passou for r in self.resultados)


# Estados possíveis ao final do pipeline automático. Nenhum deles é "aprovada":
# a aprovação é decisão humana e acontece fora desta etapa.
STATUS_EM_REVISAO = "em_revisao_humana"
STATUS_BLOQUEADA = "bloqueada"


@dataclass
class PieceResult:
    variacao: Variation
    conformidade: ConformityReport
    status: str


@dataclass
class GenerationResult:
    pecas: list[PieceResult]
    tempo_segundos: float
    tentativas_geracao: int
    versao_manual: str

    def to_dict(self) -> dict:
        return asdict(self)
