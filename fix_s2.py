# fix_s2.py —— 把 §2 两个 τ 标注移到点的右下方
import re, shutil
from pathlib import Path

SRC = Path("views/0_电路分析速览.py")
BAK = Path.home() / "Desktop" / "0_电路分析速览.py.bak"

src = SRC.read_text(encoding="utf-8")
shutil.copy(SRC, BAK)

NEW = '''for k, txt in [(1, "63.2 %"), (3, "95 %")]:
    yk = 1 - np.exp(-k)
    fig.add_trace(go.Scatter(x=[k * tau], y=[yk], mode="markers",
                             showlegend=False, hoverinfo="skip",
                             marker=dict(size=10, color=ui.ACCENT_WARM)))
    fig.add_annotation(x=k * tau, y=yk, text="t = {}τ  {}".format(k, txt),
                       showarrow=False, xshift=14, yshift=-20,
                       xanchor="left", yanchor="top",
                       font=dict(color=ui.ACCENT_WARM, size=13))
'''

pat = re.compile(r'for k, txt in \[.*?\n(?=ui\.style_fig)', re.S)
new_src, n = pat.subn(NEW + "\n", src)

if n == 0:
    print("还是没匹配上，把 §2 整段再贴一次给我。")
else:
    SRC.write_text(new_src, encoding="utf-8")
    print("已替换", n, "处，备份：", BAK)
