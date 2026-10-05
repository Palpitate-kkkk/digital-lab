"""flipflop.py —— 触发器 / 锁存器波形仿真（纯逻辑，不依赖界面）

约定
  时钟：每个周期 4 格，CLK = [0, 1, 1, 0]
        p=1、p=2 为高电平；上升沿在 p=1 那格的起点，下降沿在 p=3 那格的起点。
  输入：0/1 串按格铺开，一格一位（4 位 = 一个时钟周期）。
  采样：边沿触发取"边沿前一格"的输入值 —— 对应实际电路里的建立时间要求。
"""

PHASES = 4
CLK_PATTERN = [0, 1, 1, 0]


def parse_bits(text, length):
    """'1010 0110' -> ([1,0,1,0,0,1,1,0], [被忽略的字符])"""
    bits, bad = [], []
    for ch in (text or ""):
        if ch in "01":
            bits.append(int(ch))
        elif ch in " ,，|·":
            continue
        else:
            bad.append(ch)
    bits = bits[:length] + [0] * max(0, length - len(bits))
    return bits, bad


def clock_bits(ncells):
    return [CLK_PATTERN[i % PHASES] for i in range(ncells)]


def edges(ncells, mode):
    p = 1 if mode == "rise" else 3
    return [i for i in range(ncells) if i % PHASES == p]


def nxt(kind, before, d=0, j=0, k=0, t=0):
    """特性方程"""
    if kind == "D":
        return 1 if d else 0
    if kind == "JK":
        return (j & (1 - before)) | ((1 - k) & before)
    return t ^ before


def simulate(kind, mode, ncyc, d=None, j=None, k=None, t=None, q0=0):
    """mode: 'rise' / 'fall' / 'level'；返回逐格的各条波形"""
    ncells = ncyc * PHASES
    clk = clock_bits(ncells)
    inp = list(j) if kind == "JK" else list(d if kind == "D" else t)
    inp2 = list(k) if kind == "JK" else None
    q = [0] * ncells
    samples, prev = [], q0

    if mode == "level":                       # 高电平透明（锁存器）
        for i in range(ncells):
            if clk[i]:
                prev = inp[i]
            q[i] = prev
        ed = []
    else:                                     # 边沿触发
        ed = edges(ncells, mode)
        eset = set(ed)
        for i in range(ncells):
            if i in eset:
                a = inp[i - 1] if i else inp[0]
                b = (inp2[i - 1] if i else inp2[0]) if inp2 else None
                before = prev
                if kind == "D":
                    prev = nxt("D", before, d=a)
                    samples.append(dict(cell=i, before=before, after=prev, d=a))
                elif kind == "JK":
                    prev = nxt("JK", before, j=a, k=b)
                    samples.append(dict(cell=i, before=before, after=prev, j=a, k=b))
                else:
                    prev = nxt("T", before, t=a)
                    samples.append(dict(cell=i, before=before, after=prev, t=a))
            q[i] = prev

    return dict(clk=clk, inp=inp, inp2=inp2, q=q, qbar=[1 - v for v in q],
                edges=ed, samples=samples, ncells=ncells)


if __name__ == "__main__":
    D = parse_bits("10100110", 8)[0]
    print("输入 D =", D, "  CLK =", clock_bits(8))
    for mode, exp in (("rise", [0, 1, 1, 1, 1, 0, 0, 0]),
                      ("fall", [0, 0, 0, 1, 1, 1, 1, 1]),
                      ("level", [0, 0, 1, 1, 1, 1, 1, 1])):
        got = simulate("D", mode, 2, d=D)["q"]
        print("  {:5}  Q = {}  手算 = {}  {}".format(mode, got, exp, "OK" if got == exp else "!!!"))
    jk = simulate("JK", "rise", 2, j=parse_bits("11111111", 8)[0],
                  k=parse_bits("11111111", 8)[0])["q"]
    print("  JK=1,1 上升沿  Q =", jk, "(每个边沿翻一次)")
    print("  T=1010 上升沿  Q =", simulate("T", "rise", 2, t=parse_bits("10101010", 8)[0])["q"])
    print()
    print("对照上面 rise 和 level 两行：同一组输入，Q 完全不一样。")
