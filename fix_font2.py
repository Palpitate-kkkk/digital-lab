# fix_font2.py —— 补掉漏网的那一行（值里带单引号）
import re, shutil
from pathlib import Path

SRC = Path("ui.py")
BAK = Path.home() / "Desktop" / "ui.py.2.bak"

src = SRC.read_text(encoding="utf-8")
shutil.copy(SRC, BAK)

hits = []


def fix(m):
    v = m.group(1)
    low = v.lower()
    if "sans-serif" not in low and re.search(r'georgia|songti|宋体|\bserif\b', low):
        hits.append(v)
        return 'family="sans-serif"'
    return m.group(0)


src = re.sub(r'family\s*=\s*"([^"]*)"', fix, src)
SRC.write_text(src, encoding="utf-8")

for h in hits:
    print("已改 family:", h)
if not hits:
    print("没有新的改动")

print()
print("--- 再复查 ---")
left = [l.strip() for l in src.splitlines()
        if re.search(r'georgia|songti|宋体', l, re.I)
        or (re.search(r'\bserif\b', l) and "sans-serif" not in l)]
if left:
    for l in left:
        print("  !", l)
else:
    print("  干净了")
print()
print("备份：", BAK)
