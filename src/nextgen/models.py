"""Modelos de dados do fluxo: briefing -> produto -> variações -> conformidade -> aprovação."""
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Optional


class BriefingError(ValueError):
    def __init__(self, problems: list[str]):
        self.problems = problems
        super().__init__("; ".join(problems))


@dataclass
class Product:
    id: str
    nome: str
    categoria: str
    descricao: str
    preco_referencia: float
    preco_promocional: Optional[float]
    validade_oferta: Optional[str]        # ISO date "YYYY-MM-DD" ou None
    canais_permitidos: list[str]
    restricoes: str
    origem: str
    requer_revisao_especial: bool = False          # ← novo
    disclaimer_obrigatorio: Optional[str] = None   # ← novo

    def preco_exibicao(self) -> Optional[float]:
        return self.preco_promocional if self.preco_promocional is not None \
               else self.preco_referencia

    def formatar_preco(self) -> str:
        p = self.preco_exibicao()
        if p is None:
            return ""
        return f"R$ {p:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def oferta_valida_em(self, referencia: date | None = None) -> bool:
        if not self.validade_oferta:
            return True
        try:
            validade = date.fromisoformat(self.validade_oferta)
            hoje = referencia or date.today()
            return hoje <= validade
        except (ValueError, TypeError):
            return False  # falha fechada


@dataclass
class Briefing:
    objetivo: str
    publico: str
    formatos: list[str]
    tom: str
    produto_id: Optional[str] = None
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
            produto_id=(data.get("produto_id") or None),
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
    # Campos comerciais preenchidos pelo generator a partir do catálogo (NUNCA pelo LLM):
    produto_id: Optional[str] = None
    preco_formatado: Optional[str] = None
    validade: Optional[str] = None
    imagem_tipo: str = "ilustrativa"    # ilustrativa | produto_real | ia_gerada


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


STATUS_EM_REVISAO = "em_revisao_humana"
STATUS_BLOQUEADA = "bloqueada"
STATUS_APROVADA = "aprovada"
STATUS_REPROVADA = "reprovada"


@dataclass
class PieceResult:
    variacao: Variation
    conformidade: ConformityReport
    status: str
    decisao: Optional[dict] = None


@dataclass
class GenerationResult:
    pecas: list[PieceResult]
    tempo_segundos: float
    tentativas_geracao: int
    versao_manual: str

    def to_dict(self) -> dict:
        return asdict(self)