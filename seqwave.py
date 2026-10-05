"""seqwave —— 时序电路波形推算引擎（digital-lab 模块③）

约定
----
* 时间以「时钟周期」为单位，CP 周期 = 1
* 时间网格步长 0.25（二进制精确值，没有浮点误差）
* CP 在 [k + 0.5, k + 1) 为高，上升沿落在 t = 0.5, 1.5, 2.5, ...
* 所有触发器按「零传输延迟」处理，与 842 手画波形的习惯一致
"""

import numpy as np

DT = 0.25


def time_grid(n_periods):
    return np.arange(0.0, n_periods + DT / 2, DT)


def clock_wave(t):
    ph = np.mod(t - 0.5, 1.0)
    return np.where((t >= 0.5 - 1e-9) & (ph < 0.5), 1, 0)


def is_rising(ti):
    """该时刻是否为 CP 上升沿。"""
    if ti < 0.5 - 1e-9:
        return False
    return abs(np.mod(ti - 0.5, 1.0)) < 1e-9


def edges_of(n_periods):
    return [0.5 + k for k in range(n_periods)]


def parse_bits(s, n=8):
    """把用户输入的字符串变成 0/1 列表。"""
    bits = [1 if ch == "1" else 0 for ch in str(s) if ch in "01"]
    if not bits:
        bits = [0]
    return bits[:n]


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def sim_sync_counter(n_periods=5, **kw):
    """例① 同步模 4 计数器：两片 D 触发器共用 CP 上升沿。"""
    t = time_grid(n_periods)
    q1 = np.zeros(len(t), dtype=int)
    q2 = np.zeros(len(t), dtype=int)
    c1 = c2 = 0
    rows = []
    k = 0
    for i, ti in enumerate(t):
        if is_rising(ti):
            c1, c2 = 1 - c1, c2 ^ c1
            k += 1
            rows.append([k, str(c2) + str(c1), c2 & c1])
        q1[i], q2[i] = c1, c2
    return {
        "t": t,
        "rows": ["CP", "Q1", "Q2", "Y = Q1·Q2"],
        "signals": {"CP": clock_wave(t), "Q1": q1, "Q2": q2, "Y = Q1·Q2": q1 & q2},
        "edges": edges_of(n_periods),
        "table": md_table(["第几个时钟", "Q2 Q1（计数值）", "Y = Q1·Q2"], rows),
    }


def sim_async_counter(n_periods=5, **kw):
    """例② 异步模 4 计数器：第二级由第一级的 Q1 下降沿触发。"""
    t = time_grid(n_periods)
    q1 = np.zeros(len(t), dtype=int)
    q2 = np.zeros(len(t), dtype=int)
    c1 = c2 = 0
    prev1 = 0
    rows = []
    k = 0
    for i, ti in enumerate(t):
        if i > 0 and is_rising(ti):
            c1 = 1 - c1
            flipped = False
            if prev1 == 1 and c1 == 0:
                c2 = 1 - c2
                flipped = True
            k += 1
            rows.append([k, str(c2) + str(c1), "翻转" if flipped else "保持"])
        prev1 = c1
        q1[i], q2[i] = c1, c2
    return {
        "t": t,
        "rows": ["CP", "Q1", "Q2"],
        "signals": {"CP": clock_wave(t), "Q1": q1, "Q2": q2},
        "edges": edges_of(n_periods),
        "table": md_table(["第几个时钟", "Q2 Q1（计数值）", "Q2 的动作"], rows),
    }


def sim_shift_register(n_periods=8, data_bits=None, **kw):
    """例③ 两位串入串出移位寄存器。"""
    bits = list(data_bits) if data_bits else [1, 0, 1, 1, 0, 1, 0, 0]
    t = time_grid(n_periods)
    q1 = np.zeros(len(t), dtype=int)
    q2 = np.zeros(len(t), dtype=int)
    data = np.zeros(len(t), dtype=int)
    c1 = c2 = 0
    k = 0
    rows = []
    for i, ti in enumerate(t):
        idx = int(ti)
        data[i] = bits[idx] if idx < len(bits) else 0
        if is_rising(ti):
            d = bits[k] if k < len(bits) else 0
            c1, c2 = d, c1
            k += 1
            rows.append([k, data[i], c1, c2])
        q1[i], q2[i] = c1, c2
    return {
        "t": t,
        "rows": ["CP", "DATA", "Q1", "Q2"],
        "signals": {"CP": clock_wave(t), "DATA": data, "Q1": q1, "Q2": q2},
        "edges": edges_of(n_periods),
        "table": md_table(["第几个时钟", "送入的位", "Q1", "Q2"], rows),
    }


def sim_async_reset(n_periods=5, reset_cycle=2, **kw):
    """例④ 异步复位：RD 低电平期间 Q 恒为 0，与 CP 无关。"""
    t = time_grid(n_periods)
    start = reset_cycle + 0.75
    rd = np.where((t >= start - 1e-9) & (t < start + 0.5 - 1e-9), 0, 1)
    q1 = np.zeros(len(t), dtype=int)
    c1 = 0
    rows = []
    k = 0
    for i, ti in enumerate(t):
        if i > 0 and rd[i - 1] == 1 and rd[i] == 0:
            rows.append(["%g" % ti, "RD 拉低（异步）", 0])
        if i > 0 and rd[i - 1] == 0 and rd[i] == 1:
            rows.append(["%g" % ti, "RD 拉高", c1])
        if rd[i] == 0:
            c1 = 0
        elif is_rising(ti):
            c1 = 1 - c1
            k += 1
            rows.append(["%g" % ti, "第 %d 个 CP 上升沿" % k, c1])
        q1[i] = c1
    return {
        "t": t,
        "rows": ["CP", "RD", "Q1"],
        "signals": {"CP": clock_wave(t), "RD": rd, "Q1": q1},
        "edges": edges_of(n_periods),
        "table": md_table(["时刻（时钟周期）", "事件", "事件之后的 Q1"], rows),
    }


PRESETS = {
    "① 同步计数器（模 4）": {
        "desc": "两片 D 触发器共用 CP：D1 接 Q1 的反，D2 接 Q2 异或 Q1。状态按 00 → 01 → 10 → 11 循环，Q2 就是 CP 的四分频。",
        "params": [],
        "sim": sim_sync_counter,
    },
    "② 异步计数器（逐级分频）": {
        "desc": "第一级由 CP 上升沿触发，第二级由第一级的 Q1 下降沿触发 —— 逐级分频，两级串起来就是模 4 计数。",
        "params": [],
        "sim": sim_async_counter,
    },
    "③ 串入串出移位寄存器": {
        "desc": "两片 D 触发器串联，输入数据每个时钟移一位：Q1 比输入慢一拍，Q2 慢两拍。",
        "params": ["data"],
        "sim": sim_shift_register,
    },
    "④ 异步复位（RD 低有效）": {
        "desc": "RD 拉低时 Q 立即清零，与 CP 完全无关 —— 这就是异步复位优先级最高的含义。",
        "params": ["reset"],
        "sim": sim_async_reset,
    },
}
