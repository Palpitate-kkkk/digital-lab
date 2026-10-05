# fix_font.py —— 撤掉衬线体，全站回到系统默认无衬线字体
import re, shutil
from pathlib import Path

SRC = Path("ui.py")
BAK = Path.home() / "Desktop" / "ui.py.bak"

src = SRC.read_text(encoding="utf-8")
shutil.copy(SRC, BAK)

changed = []


def is_serif(v):
    v = v.lower()
    if "sans-serif" in v:
        return False
    return bool(re.search(r'georgia|songti|宋体|\bserif\b', v))


# 1) CSS 里 font-family: Georgia, "Songti SC", serif;  ->  整条删掉（继承 Streamlit 默认）
def drop_css(m):
    if is_serif(m.group(1)):
        changed.append("CSS    : " + m.group(0).strip())
        return ""
    return m.group(0)


src = re.sub(r'font-family\s*:\s*([^;{}\n]+);', drop_css, src)


# 2) Plotly 里 family="Georgia, Songti SC, serif"  ->  family="sans-serif"
def fix_family(m):
    if is_serif(m.group(2)):
        changed.append("PLOTLY : " + m.group(0).strip())
        return 'family=' + m.group(1) + 'sans-serif' + m.group(1)
    return m.group(0)


src = re.sub(r'family\s*=\s*(["\'])([^"\']*)\1', fix_family, src)

SRC.write_text(src, encoding="utf-8")

if changed:
    for c in changed:
        print("已改  ", c)
else:
    print("没找到衬线体声明（写法可能不太一样，往下看残留）")

print()
print("--- 复查：文件里还残留这些行 ---")
left = [l for l in src.splitlines() if re.search(r'Georgia|Songti|宋体', l)]
if left:
    for l in left:
        print("  !", l.strip())
else:
    print("  干净，没有残留")
print()
print("备份：", BAK)
