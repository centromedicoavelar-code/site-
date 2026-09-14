from geradores.marca.pack import FONT_CSS, MONT, INT, P, S, A, AR, W, T, WHITE, lettering, sub
from geradores.marca.pack_serra import serra, principal, SERRA_W, SERRA_H

TAG = "SAÚDE INTEGRADA PARA TODAS AS FASES DA VIDA"

def mark_svg(height=64, tc=P, subc=A, curve=S, back=S, front=P, sun=T):
    """Assinatura horizontal reduzida (serra + CENTRO MÉDICO + avelar) como SVG inline."""
    w = height * 697/163
    return (f'<svg viewBox="40 44 697 163" width="{w:.0f}" height="{height}" style="display:block">'
            f'{principal(1.0, tc, curve, back, front, sun, subc)}</svg>')

def serra_svg(width, back=S, front=P, sun=T, mono=False, ink=P):
    h = width * SERRA_H / SERRA_W
    return (f'<svg viewBox="0 0 {SERRA_W} {SERRA_H}" width="{width:.0f}" height="{h:.0f}" style="display:block">'
            f'{serra(0, 0, 1.0, back, front, sun, mono, ink)}</svg>')

BASE_CSS = f"""
{FONT_CSS}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{margin:0;background:#888}}
.post{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{W};font-family:'Inter',Arial,sans-serif;color:{A}}}
.story{{width:1080px;height:1920px;position:relative;overflow:hidden;background:{W};font-family:'Inter',Arial,sans-serif}}
.mont{{font-family:'Montserrat',Arial,sans-serif}}
h1{{font-family:'Montserrat',Arial,sans-serif;font-weight:800;color:{P};letter-spacing:-1.5px;line-height:1.06}}
.sub{{font-weight:400;color:{A};line-height:1.42}}
.selo{{display:inline-block;background:{T};color:{W};font-family:'Montserrat',Arial,sans-serif;font-weight:700;
       font-size:24px;letter-spacing:2.5px;padding:16px 30px;border-radius:999px;text-transform:uppercase}}
.selo.ghost{{background:transparent;border:3px solid {T};color:{T}}}
.tag{{font-weight:600;font-size:19px;letter-spacing:1.8px;color:{P};text-transform:uppercase}}
.foot{{position:absolute;left:80px;right:80px;bottom:76px;display:flex;justify-content:space-between;align-items:flex-end;gap:40px}}
.foot .tag{{max-width:720px;line-height:1.5;font-size:17px;letter-spacing:1.6px;white-space:nowrap}}
.inv h1,.inv .tag{{color:{W}}} .inv .sub{{color:{S}}}
.small{{font-size:20px;color:#5f6f6e;line-height:1.5}}
.inv .small{{color:{S}}}
"""
