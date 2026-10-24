import html
from typing import Callable
from .manual import Manual
from .models import PieceResult, Product

ESC = html.escape

def _paleta(manual: Manual) -> dict:
    return {p["nome"]: p["hex"] for p in manual.paleta}

def _rodape(v, product) -> str:
    partes = [f"Imagem: {ESC(v.imagem_tipo)}"]
    if product: partes.append(f"SKU: {ESC(product.id)}")
    return " · ".join(partes)

def _bloco_preco(v) -> str:
    if not v.preco_formatado and not v.validade: return ""
    preco = f'<div class="preco">{ESC(v.preco_formatado)}</div>' if v.preco_formatado else ""
    
    validade = ""
    if v.validade:
        try:
            from datetime import datetime
            data_obj = datetime.strptime(v.validade, "%Y-%m-%d")
            validade_str = data_obj.strftime("%d/%m/%Y")
        except:
            validade_str = v.validade
        validade = f'<div class="validade">Válida até {validade_str}</div>'
        
    return f'<div class="box-preco">{preco}{validade}</div>'

def _html_base(css: str, corpo: str) -> str:
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
  body {{ margin:0; font-family: 'Inter', sans-serif; background:#f4f6f8; display:flex; justify-content:center; align-items:center; min-height:100vh; }}
  .peca {{ position:relative; overflow:hidden; box-sizing:border-box; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }}
  .titulo {{ font-weight:900; line-height:1.1; letter-spacing:-0.5px; }}
  .texto {{ line-height:1.4; font-weight:400; }}
  .cta {{ display:inline-block; font-weight:700; border-radius:8px; text-transform:uppercase; font-size:12px; letter-spacing:1px; }}
  .preco {{ font-weight:900; font-size:32px; line-height:1; }}
  .validade {{ font-size:11px; opacity:0.8; margin-top:4px; }}
  .rodape-meta {{ position:absolute; bottom:8px; left:16px; right:16px; font-size:10px; opacity:0.5; text-align:center; }}
  {css}
</style></head><body>{corpo}</body></html>"""

# ==========================================
# FEED SOCIAL (Quadrado)
# ==========================================
def _feed_social(peca, product, manual, variante=1):
    v, p = peca.variacao, _paleta(manual)
    azul = p.get("azul principal", "#0B5FA5")
    vermelho = p.get("vermelho", "#D32F2F")
    branco = p.get("branco", "#FFF")

    if variante == 1: # Full Bleed Blue com detalhe vermelho
        css = f""".peca {{ width:600px; height:600px; background:{azul}; color:{branco}; display:flex; flex-direction:column; justify-content:flex-end; padding:50px; }}
        .shape {{ position:absolute; top:-50px; right:-50px; width:300px; height:300px; background:{vermelho}; border-radius:50%; opacity:0.9; }}
        .titulo {{ font-size:48px; margin-bottom:16px; z-index:2; }}
        .texto {{ font-size:18px; margin-bottom:24px; max-width:80%; z-index:2; }}
        .row {{ display:flex; align-items:center; justify-content:space-between; z-index:2; }}
        .cta {{ background:{vermelho}; color:{branco}; padding:14px 24px; border-radius:40px; font-size:14px; }}"""
        corpo = f"""<div class="peca"><div class="shape"></div>
        <div class="titulo">{ESC(v.titulo)}</div><div class="texto">{ESC(v.texto)}</div>
        <div class="row"><div class="cta">{ESC(v.cta)}</div>{_bloco_preco(v)}</div>
        <div class="rodape-meta">{_rodape(v, product)}</div></div>"""
        return _html_base(css, corpo)

    if variante == 2: # Split Clean (Esquerda Branca, Direita Vermelha)
        css = f""".peca {{ width:600px; height:600px; background:{branco}; display:flex; }}
        .lado-esq {{ width:60%; padding:40px; display:flex; flex-direction:column; justify-content:space-between; color:{azul}; }}
        .lado-dir {{ width:40%; background:{vermelho}; display:flex; align-items:center; justify-content:center; color:{branco}; font-weight:700; font-size:20px; }}
        .titulo {{ font-size:38px; }}
        .texto {{ font-size:16px; color:#555; }}
        .cta {{ background:{azul}; color:{branco}; padding:14px 24px; text-align:center; border-radius:8px; }}"""
        corpo = f"""<div class="peca">
        <div class="lado-esq"><div class="titulo">{ESC(v.titulo)}</div><div class="texto">{ESC(v.texto)}</div>
        <div>{_bloco_preco(v)}<div class="cta" style="margin-top:20px;">{ESC(v.cta)}</div></div></div>
        <div class="lado-dir">Imagem</div>
        <div class="rodape-meta" style="color:{azul};">{_rodape(v, product)}</div></div>"""
        return _html_base(css, corpo)

    # variante == 3: Minimalist Center (Fundo Branco, Borda Azul)
    css = f""".peca {{ width:600px; height:600px; background:{branco}; padding:60px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; color:{azul}; border: 20px solid {azul}; }}
    .titulo {{ font-size:52px; margin-bottom:20px; color:{azul}; }}
    .texto {{ font-size:18px; max-width:80%; margin-bottom:30px; color:#555; }}
    .cta {{ background:{vermelho}; color:{branco}; padding:16px 32px; border-radius:4px; font-weight:900; }}"""
    corpo = f"""<div class="peca"><div class="titulo">{ESC(v.titulo)}</div><div class="texto">{ESC(v.texto)}</div>
    <div class="cta">{ESC(v.cta)}</div><div style="margin-top:30px;">{_bloco_preco(v)}</div>
    <div class="rodape-meta">{_rodape(v, product)}</div></div>"""
    return _html_base(css, corpo)

# ==========================================
# STORY (9:16)
# ==========================================
def _story(peca, product, manual, variante=1):
    v, p = peca.variacao, _paleta(manual)
    azul = p.get("azul principal", "#0B5FA5")
    vermelho = p.get("vermelho", "#D32F2F")
    branco = p.get("branco", "#FFF")

    if variante == 1: # Top Solid, Bottom White
        css = f""".peca {{ width:360px; height:640px; background:{branco}; display:flex; flex-direction:column; }}
        .topo {{ height:55%; background:{azul}; position:relative; }}
        .conteudo {{ height:45%; padding:30px; display:flex; flex-direction:column; justify-content:space-between; color:{azul}; }}
        .titulo {{ font-size:28px; }} .texto {{ font-size:14px; color:#666; }}
        .cta {{ background:{vermelho}; color:{branco}; padding:16px; text-align:center; border-radius:8px; }}"""
        corpo = f"""<div class="peca"><div class="topo"></div><div class="conteudo">
        <div><div class="titulo">{ESC(v.titulo)}</div><div class="texto">{ESC(v.texto)}</div></div>
        <div>{_bloco_preco(v)}<div class="cta">{ESC(v.cta)}</div></div></div>
        <div class="rodape-meta">{_rodape(v, product)}</div></div>"""
        return _html_base(css, corpo)

    if variante == 2: # Full Red (Impacto)
        css = f""".peca {{ width:360px; height:640px; background:{vermelho}; padding:40px 30px; display:flex; flex-direction:column; justify-content:space-between; color:{branco}; text-align:center; }}
        .titulo {{ font-size:36px; margin-top:40px; font-weight:900; }}
        .texto {{ font-size:16px; background:{branco}; color:{azul}; padding:15px; border-radius:10px; font-weight:600; }}
        .cta {{ background:{azul}; color:{branco}; padding:16px; border-radius:40px; }}"""
        corpo = f"""<div class="peca"><div class="titulo">{ESC(v.titulo)}</div>
        <div><div class="texto">{ESC(v.texto)}</div><div style="margin-top:20px;">{_bloco_preco(v)}</div></div>
        <div class="cta">{ESC(v.cta)}</div><div class="rodape-meta">{_rodape(v, product)}</div></div>"""
        return _html_base(css, corpo)

    # variante == 3: Photo Frame Clean
    css = f""".peca {{ width:360px; height:640px; background:{branco}; padding:20px; display:flex; flex-direction:column; }}
    .frame {{ border: 4px solid {azul}; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:30px; position:relative; background:{branco}; z-index:2; }}
    .bg-shape {{ position:absolute; top:0; left:0; width:100%; height:40%; background:{azul}; z-index:1; }}
    .titulo {{ font-size:32px; color:{azul}; margin-top:40px; text-align:center; }}
    .texto {{ font-size:15px; color:#555; text-align:center; }}
    .cta {{ background:{vermelho}; color:{branco}; padding:14px; text-align:center; border-radius:8px; }}"""
    corpo = f"""<div class="peca"><div class="bg-shape"></div><div class="frame">
    <div class="titulo">{ESC(v.titulo)}</div><div class="texto">{ESC(v.texto)}</div>
    <div>{_bloco_preco(v)}<div class="cta" style="margin-top:20px;">{ESC(v.cta)}</div></div>
    </div><div class="rodape-meta" style="z-index:3;">{_rodape(v, product)}</div></div>"""
    return _html_base(css, corpo)

# ==========================================
# BANNER WEB (Horizontal)
# ==========================================
def _banner_web(peca, product, manual, variante=1):
    v, p = peca.variacao, _paleta(manual)
    azul = p.get("azul principal", "#0B5FA5")
    vermelho = p.get("vermelho", "#D32F2F")
    branco = p.get("branco", "#FFF")

    if variante == 1: # Clean Split (Borda Azul)
        css = f""".peca {{ width:728px; height:90px; background:{branco}; display:flex; align-items:center; border: 2px solid {azul}; }}
        .txt {{ flex:1; padding:0 20px; display:flex; align-items:center; gap:15px; color:{azul}; }}
        .titulo {{ font-size:20px; }} .texto {{ font-size:13px; opacity:0.8; }}
        .cta-box {{ background:{vermelho}; color:{branco}; height:100%; padding:0 30px; display:flex; align-items:center; justify-content:center; }}"""
        corpo = f"""<div class="peca"><div class="txt">
        <div class="titulo">{ESC(v.titulo)}</div><div class="texto">{ESC(v.texto)}</div></div>
        <div style="margin-right:20px;">{_bloco_preco(v)}</div>
        <div class="cta-box">{ESC(v.cta)}</div><div class="rodape-meta" style="color:{azul}; text-align:left;">{_rodape(v, product)}</div></div>"""
        return _html_base(css, corpo)

    if variante == 2: # Full Dark (Azul Sólido)
        css = f""".peca {{ width:728px; height:90px; background:{azul}; color:{branco}; display:flex; align-items:center; justify-content:space-between; padding:0 30px; }}
        .titulo {{ font-size:24px; font-weight:900; }} .texto {{ font-size:14px; opacity:0.9; }}
        .cta {{ background:{vermelho}; color:{branco}; padding:10px 20px; border-radius:4px; font-size:14px; }}"""
        corpo = f"""<div class="peca"><div><div class="titulo">{ESC(v.titulo)}</div><div class="texto">{ESC(v.texto)}</div></div>
        <div style="display:flex; align-items:center; gap:30px;">{_bloco_preco(v)}<div class="cta">{ESC(v.cta)}</div></div>
        <div class="rodape-meta">{_rodape(v, product)}</div></div>"""
        return _html_base(css, corpo)

    # variante == 3: Alert Bar (Faixa Vermelha em cima)
    css = f""".peca {{ width:728px; height:90px; background:{branco}; display:flex; flex-direction:column; }}
    .topo {{ background:{vermelho}; color:{branco}; padding:6px 20px; font-size:11px; font-weight:900; text-transform:uppercase; letter-spacing:1px; }}
    .baixo {{ flex:1; display:flex; align-items:center; justify-content:space-between; padding:0 20px; color:{azul}; }}
    .titulo {{ font-size:22px; }} .texto {{ font-size:12px; }}
    .cta {{ border: 2px solid {azul}; padding:8px 20px; border-radius:4px; font-weight:700; }}"""
    corpo = f"""<div class="peca"><div class="topo">Oferta Especial</div>
    <div class="baixo"><div><div class="titulo">{ESC(v.titulo)}</div><div class="texto">{ESC(v.texto)}</div></div>
    <div style="display:flex; align-items:center; gap:20px;">{_bloco_preco(v)}<div class="cta">{ESC(v.cta)}</div></div></div>
    <div class="rodape-meta">{_rodape(v, product)}</div></div>"""
    return _html_base(css, corpo)

_RENDERERS = {"feed_social": _feed_social, "story": _story, "banner_web": _banner_web}
VARIANTES = {"feed_social": 3, "story": 3, "banner_web": 3}

def render_peca(peca, product, manual, variante=1):
    renderer = _RENDERERS.get(peca.variacao.formato)
    if renderer is None: raise ValueError(f"Formato inválido: {peca.variacao.formato}")
    variante = max(1, min(variante, VARIANTES[peca.variacao.formato]))
    return renderer(peca, product, manual, variante)