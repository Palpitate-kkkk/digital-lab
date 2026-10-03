# patch_labels.py —— 把 §2 里两个 τ 标注从曲线上挪开
import re, shutil
from pathlib import Path

SRC = Path("views/0_电路分析速览.py")
BAK = Path.home() / "Desktop" / "0_电路分析速览.py.bak"

text = SRC.read_text(encoding="utf-8")
shutil.copy(SRC, BAK)

i2 = text.index("## §2")
i3 = text.index("## §3")
head, mid, tail = text[:i2], text[i2:i3], text[i3:]


def spans(s, name):
    out = []
    for m in re.finditer(re.escape(name), s):
        j, d = m.end() - 1, 0
        while j < len(s):
            c = s[j]
            if c in "([{":
                d += 1
            elif c in ")]}":
                d -= 1
                if d == 0:
                    break
            j += 1
        out.append((m.start(), j + 1, s[m.start():j + 1]))
    return out


log = []

for s, e, blk in reversed(spans(mid, "add_annotation(")):
    if ("63.2" in blk or "95" in blk) and "yshift" not in blk:
        core = blk[:-1].rstrip().rstrip(",")
        mid = mid[:s] + core + ', xshift=46, yshift=-22, xanchor="left", yanchor="middle")' + mid[e:]
        log.append("add_annotation -> 加像素偏移")

for s, e, blk in reversed(spans(mid, "Scatter(")):
    if ("63.2" in blk or "95" in blk) and "textposition" in blk:
        new = re.sub(r'textposition\s*=\s*"[^"]*"', 'textposition="bottom right"', blk)
        if new != blk:
            mid = mid[:s] + new + mid[e:]
            log.append('Scatter -> textposition="bottom right"')

if not log:
    print("没在 §2 里找到标注代码。")
    print("请把 §2 那一段（从 ## §2 到 ## §3）整段复制发给我。")
else:
    SRC.write_text(head + mid + tail, encoding="utf-8")
    for L in log:
        print("OK", L)
    print()
    print("改完了。原文件已备份：", BAK)
