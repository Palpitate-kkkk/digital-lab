"""kmap.py —— 卡诺图化简核心算法

纯逻辑：不依赖 Streamlit / Plotly，可以直接 python3 kmap.py 自检。
变量按 A(高位) ... 末尾位 排列，K-map 行列都用格雷码排列。
"""

import itertools
import re
from itertools import product


# ---------- 1. 卡诺图布局 ----------

def gray_seq(nbits):
    """n 位格雷码序列：2 位 -> [0, 1, 3, 2]"""
    return [i ^ (i >> 1) for i in range(1 << nbits)]


def layout(n):
    """n 变量时 (行位数, 列位数)：2->1x1, 3->1x2, 4->2x2, 5->2x3"""
    col = 2 if n >= 3 else 1
    return n - col, col


def grid(n):
    """返回 (rows, cols, cells)；cells[r][c] 是该格对应的最小项编号"""
    rb, cb = layout(n)
    rows, cols = gray_seq(rb), gray_seq(cb)
    cells = [[(r << cb) | c for c in cols] for r in rows]
    return rows, cols, cells


# ---------- 2. 乘积项与覆盖 ----------

def cover(spec):
    """spec 形如 '1-0-'（每位 0/1/-），返回它覆盖的最小项集合"""
    n = len(spec)
    free = [i for i, s in enumerate(spec) if s == "-"]
    base = 0
    for i, s in enumerate(spec):
        if s == "1":
            base |= 1 << (n - 1 - i)
    out = set()
    for k in range(1 << len(free)):
        m = base
        for j, i in enumerate(free):
            if (k >> j) & 1:
                m |= 1 << (n - 1 - i)
        out.add(m)
    return out


def all_specs(n):
    for p in product("01-", repeat=n):
        yield "".join(p)


def prime_implicants(n, ones, dcs=()):
    """所有质蕴含项：[(spec, 覆盖集合), ...]"""
    allowed = set(ones) | set(dcs)
    valid = [(s, cover(s)) for s in all_specs(n)]
    valid = [(s, c) for s, c in valid if c <= allowed]
    return [(s, c) for s, c in valid if not any(o > c for _, o in valid)]


def minimize(n, ones, dcs=()):
    """返回最简与或式用到的质蕴含项 [(spec, 覆盖到的1), ...]"""
    ones = set(ones)
    if not ones:
        return []
    primes = [(s, c & ones) for s, c in prime_implicants(n, ones, dcs)]
    primes = [(s, c) for s, c in primes if c]
    best = []

    def dfs(rem, picked):
        nonlocal best
        if best and len(picked) >= len(best):
            return
        if not rem:
            best = picked[:]
            return
        # 挑一个最"难缠"的 1：能被覆盖它的圈最少
        m = min(rem, key=lambda x: sum(1 for _, c in primes if x in c))
        cand = sorted((t for t in primes if m in t[1]), key=lambda t: -len(t[1] & rem))
        for s, c in cand:
            picked.append((s, c))
            dfs(rem - c, picked)
            picked.pop()

    dfs(set(ones), [])
    return best


# ---------- 3. 表达式书写 ----------

def term_str(spec, names="ABCDE"):
    parts = []
    for v, s in zip(names, spec):
        if s == "1":
            parts.append(v)
        elif s == "0":
            parts.append(v + "'")
    return "".join(parts) or "1"


def expr_str(picked, names="ABCDE"):
    if not picked:
        return "0"
    terms = [term_str(s, names) for s, _ in picked]
    if "1" in terms:
        return "1"
    return " + ".join(terms)


# ---------- 4. 圈的几何（给画图用） ----------

def _runs(vals, total):
    """把一组下标切成若干连续段；首尾相接（环绕）时拆成两块"""
    vals = sorted(set(vals))
    if not vals:
        return []
    if len(vals) == total:
        return [(0, total - 1)]
    out, cur = [], [vals[0]]
    for v in vals[1:]:
        if v == cur[-1] + 1:
            cur.append(v)
        else:
            out.append((cur[0], cur[-1]))
            cur = [v]
    out.append((cur[0], cur[-1]))
    if len(out) > 1 and out[0][0] == 0 and out[-1][1] == total - 1:
        first, last = out.pop(0), out.pop()
        out.insert(0, (last[0], total - 1))
        out.append((0, first[1]))
    return out


def group_rects(n, cov):
    """把一个圈转成若干矩形 (r0, r1, c0, c1)，跨边界会拆成两块"""
    rows, cols, cells = grid(n)
    R, C = len(rows), len(cols)
    rs = sorted({r for r in range(R) for c in range(C) if cells[r][c] in cov})
    cs = sorted({c for r in range(R) for c in range(C) if cells[r][c] in cov})
    return [(a, b, c, d) for (a, b) in _runs(rs, R) for (c, d) in _runs(cs, C)]


# ---------- 5. 输入解析 ----------

def parse_list(text, n):
    """'0,1,2,5' -> ({0,1,2,5}, [越界的值])"""
    out, bad = set(), []
    for t in re.split(r"[^0-9]+", text or ""):
        if t == "":
            continue
        v = int(t)
        if 0 <= v < (1 << n):
            out.add(v)
        else:
            bad.append(v)
    return out, bad


# ---------- 6. 自检 ----------

if __name__ == "__main__":
    cases = [
        (3, {1, 3, 5, 7}, set(), "C"),
        (4, {0, 1, 4, 5, 8, 9, 12, 13}, set(), "C'"),
        (4, {0, 1, 2, 5, 7}, set(), "3 项"),
        (4, {0, 1, 2, 5, 7}, {3}, "2 项（无关项帮忙）"),
    ]
    for n, ones, dcs, expect in cases:
        picked = minimize(n, ones, dcs)
        print("n =", n, " Σm =", sorted(ones), " Σd =", sorted(dcs))
        print("   最简式：F =", expr_str(picked))
        for s, c in picked:
            print("     圈", term_str(s).ljust(6), "覆盖", sorted(c))
        print("   预期：", expect)
        print()
