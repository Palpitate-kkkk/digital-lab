"""views/2_触发器波形.py —— 边沿触发 vs 电平触发"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import flipflop as ff
import ui

MODES = ["上升沿触发", "下降沿触发", "电平触发（高电平透明）"]
M2K = {"上升沿触发": "rise", "下降沿触发": "fall", "电平触发（高电平透明）": "level"}

PRESETS = [
    ("例① D·上升沿", "D", "上升沿触发", 4, "1010011011000001", "", ""),
    ("例② D·电平", "D", "电平触发（高电平透明）", 4, "1010011011000001", "", ""),
    ("例③ JK 翻转", "JK", "上升沿触发", 2, "", "11111111", "11111111"),
    ("例④ T 触发器", "T", "上升沿触发", 2, "10101010", "", ""),
]

EQUATIONS = {"D": "Q* = D", "JK": "Q* = JQ' + K'Q", "T": "Q* = T ⊕ Q"}
TABLES = {
    "D": "| D | Q* |\n|---|---|\n| 0 | 0 |\n| 1 | 1 |",
    "JK": "| J | K | Q* |\n|---|---|---|\n| 0 | 0 | Q 保持 |\n| 0 | 1 | 0 置 0 |\n| 1 | 0 | 1 置 1 |\n| 1 | 1 | Q' 翻转 |",
    "T": "| T | Q* |\n|---|---|\n| 0 | Q 保持 |\n| 1 | Q' 翻转 |",
}


def build_fig(sim, kind, mode, ncyc):
    ncells = sim["ncells"]
    rows = 5 if kind == "JK" else 4
    titles = ["CP（时钟）"] + (["J", "K"] if kind == "JK" else [kind]) + ["Q", "Q'"]
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True,
                        vertical_spacing=0.075, subplot_titles=titles)
    x = list(range(ncells + 1))

    def put(y, r, color, width=2.4, dash=None):
        fig.add_trace(go.Scatter(x=x, y=list(y) + [y[-1]], mode="lines", line_shape="hv",
                                 line=dict(color=color, width=width, dash=dash),
                                 showlegend=False, hoverinfo="skip"), row=r, col=1)

    put(sim["clk"], 1, ui.NAVY, 2.8)
    if kind == "JK":
        put(sim["inp"], 2, ui.ACCENT)
        put(sim["inp2"], 3, ui.ACCENT)
        qrow = 4
    else:
        put(sim["inp"], 2, ui.ACCENT)
        qrow = 3
    put(sim["q"], qrow, ui.ACCENT_WARM, 2.8)
    put(sim["qbar"], qrow + 1, ui.STEEL, 2.0, dash="dot")

    if mode == "level":
        for c in range(ncyc):
            fig.add_vrect(x0=4 * c + 1, x1=4 * c + 3, fillcolor="rgba(59,110,165,0.08)",
                          line_width=0, layer="below", row="all", col="all")
    for e in sim["edges"]:
        fig.add_vline(x=e, line=dict(color="#C6D7E8", dash="dot", width=1.2),
                      row="all", col="all")

    fig.update_layout(template="simple_white", height=140 * rows + 60, showlegend=False,
                      font=dict(family="sans-serif", color=ui.INK, size=12.5),
                      margin=dict(l=10, r=10, t=60, b=10))
    fig.update_yaxes(range=[-0.3, 1.3], tickvals=[0, 1], tickfont=dict(size=11))
    fig.update_xaxes(range=[0, ncells], tickvals=list(range(0, ncells + 1, 4)),
                     tickfont=dict(size=11))
    fig.update_xaxes(title_text="时间（格）· 每 4 格 = 1 个时钟周期", row=rows, col=1)
    return fig


ui.hero("触发器波形", "同一组输入，边沿触发和电平触发的 Q 完全不是一条波形",
        ["ZJU 842", "§ 2", "FLIP-FLOP"])

for _k, _v in (("ff_mode", "上升沿触发"), ("ff_kind", "D"), ("ff_n", 4),
               ("ff_d", "1010011011000001"), ("ff_j", "11111111"), ("ff_k", "11111111")):
    if _k not in st.session_state:
        st.session_state[_k] = _v

st.markdown("## §1 参数")
_bc = st.columns(len(PRESETS))
for _c, (_lb, _kd, _md, _n, _d, _j, _k) in zip(_bc, PRESETS):
    if _c.button(_lb, key="ffp_" + _lb):
        st.session_state["ff_mode"] = _md
        st.session_state["ff_kind"] = _kd
        st.session_state["ff_n"] = _n
        st.session_state["ff_d"] = _d
        st.session_state["ff_j"] = _j
        st.session_state["ff_k"] = _k

c1, c2 = st.columns(2)
with c1:
    mode_label = st.radio("触发方式", MODES, key="ff_mode")
with c2:
    _valid = ["D"] if mode_label.startswith("电平") else ["D", "JK", "T"]
    if st.session_state.get("ff_kind") not in _valid:
        st.session_state["ff_kind"] = _valid[0]
    kind = st.radio("触发器", _valid, key="ff_kind")
ncyc = st.slider("时钟周期数", 2, 5, key="ff_n")

need = ncyc * 4
if kind == "JK":
    t1, t2 = st.columns(2)
    jtext = t1.text_input("输入 J（{} 位，逗号可省）".format(need), key="ff_j")
    ktext = t2.text_input("输入 K（{} 位，逗号可省）".format(need), key="ff_k")
    dtext = ""
else:
    dtext = st.text_input("输入 {}（{} 位，逗号可省）".format(kind, need), key="ff_d")
    jtext = ktext = ""

dbits, bad1 = ff.parse_bits(dtext, need)
jbits, bad2 = ff.parse_bits(jtext, need)
kbits, bad3 = ff.parse_bits(ktext, need)
_bad = sorted(set(bad1 + bad2 + bad3))
if _bad:
    st.warning("这些字符看不懂，已忽略：{}".format(" ".join(_bad)))

if kind == "JK":
    sim = ff.simulate("JK", M2K[mode_label], ncyc, j=jbits, k=kbits)
else:
    sim = ff.simulate(kind, M2K[mode_label], ncyc, d=dbits, t=dbits)

st.markdown("## §2 波形")
st.plotly_chart(build_fig(sim, kind, M2K[mode_label], ncyc), width="stretch")
if M2K[mode_label] == "level":
    st.caption("浅蓝底是 CP = 1 的**透明窗口**：这段时间里 Q 一路跟着输入走；CP 一降下来就把最后的值锁住。")
else:
    st.caption("虚线 = 时钟边沿。边沿触发器的 Q **只在虚线处**才可能变化，两条虚线之间必须是水平线。")

st.markdown("## §3 状态转移")
st.markdown("**特性方程**：`{}`".format(EQUATIONS[kind]))
st.markdown("**特性表**")
st.markdown(TABLES[kind])

if sim["samples"]:
    st.markdown("**逐拍明细**（采样看的是“边沿前一刻”的值）")
    rows = []
    for i, s in enumerate(sim["samples"], 1):
        r = {"第几拍": i, "边沿在格": s["cell"], "现态 Q": s["before"]}
        if kind == "D":
            r["边沿前 D"] = s["d"]
        elif kind == "JK":
            r["边沿前 J"] = s["j"]
            r["边沿前 K"] = s["k"]
        else:
            r["边沿前 T"] = s["t"]
        r["次态 Q*"] = s["after"]
        rows.append(r)
    st.dataframe(rows)
else:
    st.caption("电平触发没有“采样时刻”这一说：CP = 1 期间 Q 一直跟着输入，CP 下降后锁住 —— 所以它不画转移表。")

st.markdown("## §4 842 考点速记")

with st.expander("① 触发器 vs 锁存器（本页的主角）"):
    st.markdown("""
- **锁存器（latch）= 电平触发**：CP 在有效电平期间"透明"，Q 一路跟着输入走；电平一失效就把最后的值锁住。
- **触发器（flip-flop）= 边沿触发**：只在时钟边沿的**那一瞬间**采样，其余时间 Q 和输入毫无关系。
- 怎么判断题目说的是哪种：出现"上升沿 / 下降沿触发"就是边沿；出现"高电平触发 / CP=1 期间导通"就是电平（锁存器）。
- 工程上为什么用边沿触发：电平触发时 Q 会反馈到输入端，CP 有效期间可能翻好几次（**空翻**），时序不可控。
- **本页的看家对比**：把触发方式在"上升沿"和"电平"之间来回切（例① / 例②），同一组输入，Q 是两条完全不同的波形。
""")

with st.expander("② 特性方程 · 特性表 · 驱动表"):
    st.markdown("""
**特性方程**（由现态 Q 求次态 Q*）
- D 触发器：`Q* = D`
- JK 触发器：`Q* = JQ' + K'Q`（00 保持 / 01 置 0 / 10 置 1 / 11 翻转）
- T 触发器：`Q* = T ⊕ Q`（T=1 翻转，T=0 保持）；`J=K=1` 的 JK 就是 T' 触发器

**驱动表**（由 Q → Q* 反推该给什么输入）—— 做"用 JK 实现 D / T"这类题的钥匙
| Q → Q* | D | J | K | T |
|---|---|---|---|---|
| 0 → 0 | 0 | 0 | × | 0 |
| 0 → 1 | 1 | 1 | × | 1 |
| 1 → 0 | 0 | × | 1 | 1 |
| 1 → 1 | 1 | × | 0 | 0 |
""")

with st.expander("③ 波形题三步画法（842 高频大题）"):
    st.markdown("""
1. 先画 CP（题干给了宽度就照抄）；
2. 在**有效边沿**处打竖虚线（说上升沿就只打上升沿，说下降沿就只打下降沿）；
3. 每碰到一条虚线做一次查表：拿**边沿前一刻**输入的稳定值 + 当前 Q，查特性表得 Q*，然后 Q 从这条虚线起保持到下一条虚线。

**铁律**：边沿触发器的 Q 在两条虚线之间必须是**一条水平线**。这是判卷第一眼看的地方。

**建立时间 t_su / 保持时间 t_h**：输入必须在边沿前后一小段时间内稳定，否则触发器可能进入**亚稳态**。
本工具故意把"输入变化"和"时钟边沿"错开半格（边沿采的是前一格的值），就是在模拟这条规矩。
""")

with st.expander("④ 空翻与主从触发器"):
    st.markdown("""
- **空翻**：电平触发时，CP 有效期间 Q 翻转后输入还在，Q 被反馈又翻回来 → 一个 CP 内翻好几次。
- **主从触发器（master-slave）**：两级锁存器串起来 —— CP=1 时主级透明、从级保持；CP 下降时主级锁存、从级接收。
  所以主从 JK 的输出在 **CP 下降沿**更新。它治好了空翻，但仍属"脉冲触发"，对 CP 宽度有要求。
- 真正的边沿触发靠内部延迟，只在边沿那一瞬动作，跟 CP 宽度无关。
- 常考：主从 JK 的输出在哪个边沿变？（**下降沿**）· 主从触发和边沿触发差在哪？
""")

with st.expander("⑤ 电路符号怎么认"):
    st.markdown("""
- CP 端有**小圆圈** → 低电平有效 / 下降沿触发；
- CP 端有**三角形**（动态输入符号）→ 边沿触发；三角形 + 小圆圈 → 下降沿触发；
- **既无圆圈也无三角形** → 电平触发（锁存器）。
- Q 与 Q' 永远互补；题目只画 Q 时不要自己补一个 Q' 上去。
""")

with st.expander("⑥ 易错点"):
    st.markdown("""
- 把边沿触发画成"输入一变 Q 就变"—— **最常见**的失分；
- 上升沿 / 下降沿看错；
- 初态没按题意取（题目不说就取 Q = 0）；
- 采样时刻看错：应该看**边沿之前**输入的稳定值；
- 忘了 Q' 只是 Q 的反相，把它当成独立信号；
- 多级电路（计数器、移位寄存器）里每一级都在**同一个边沿**同时动作 —— 这正是同步时序电路的前提。
""")

ui.rule_caption("flipflop.py：逐格离散仿真 · 边沿采样前一刻的值 · 支持 D/JK/T 与三种触发方式")
