"""Estimativa de ganho de produtividade.

Premissas explícitas:
- `tempo_manual_min` é informado pelo usuário — **estimativa**, não medição.
- `tempo_assistido_seg` é medido no protótipo (`GenerationResult.tempo_segundos`).
- O resultado NÃO prova ganho operacional real da empresa; compara hipóteses.
"""


def estimar_ganho(tempo_manual_min_por_peca: float, num_pecas: int,
                  tempo_assistido_seg: float) -> dict:
    if num_pecas <= 0:
        return {"erro": "informe ao menos uma peça gerada"}
    if tempo_manual_min_por_peca <= 0:
        return {"erro": "informe o tempo manual estimado por peça (min)"}

    manual_total = tempo_manual_min_por_peca * num_pecas
    assistido_min = tempo_assistido_seg / 60.0
    reducao_pct = ((manual_total - assistido_min) / manual_total) * 100.0

    return {
        "tempo_manual_total_min": round(manual_total, 2),
        "tempo_assistido_min": round(assistido_min, 2),
        "reducao_pct": round(reducao_pct, 1),
        "num_pecas": num_pecas,
        "premissa": "tempo manual informado (estimativa); tempo assistido medido no protótipo",
    }