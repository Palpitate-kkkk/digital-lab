"""模块③ 时序波形图工具：给一个电路、一段数据，逐拍推算出每一级的波形。"""

import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import seqwave as sw
import ui

C_CP = "#1E3A5F"
C_Q = "#3B6EA5"
C_Q2 = "#7BA4CE"
C_STEEL = "#8A9BAA"
C_WARM = "#B0413E"
C_GRID = "#DCE3EA"

ROW_COLOR = {
    "CP": C_CP,
    "Q1": C_Q,
    "Q2": C_Q2,
    "DATA": C_STEEL,
    "RD": C_STEEL,
    "Y = Q1·Q2": C_WARM,
}


def picker(label, options, key):
    """横向选择器：新版用 segmented_control，老版退回 radio。"""
    if hasattr(st, "segmented_control"):
        return st.segmented_control(label, options, default=options[0], key=key)
    return st.radio(label, options, index=0, horizontal=True, key=key)


def show_fig(fig):
    """兼容 st.plotly_chart 的参数改名。"""
    try:
        st.plotly_chart(fig, width="stretch")
    except Exception:
        st.plotly_chart(fig, use_container_width=True)


ui.hero(
    "时序波形图工具",
    "给一个电路、一段数据，逐拍推算出每一级的波形 —— 842 大题就是这么画的",
    ["ZJU 842", "§ 3", "P0 · 必考"],
)

st.markdown("## §1 参数")

names = list(sw.PRESETS.keys())
choice = picker("选择电路", names, "circuit")
preset = sw.PRESETS[choice]
st.caption(preset["desc"])

col1, col2 = st.columns(2)
with col1:
    default_n = 8 if "data" in preset["params"] else 5
    n_periods = st.slider("时钟周期数", 2, 8, default_n, key="n_" + choice)

kwargs = {}
with col2:
    if "data" in preset["params"]:
        raw = st.text_input("输入数据序列（每个时钟送 1 位，最多 8 位）", "10110100", key="bits")
        kwargs["data_bits"] = sw.parse_bits(raw)
    elif "reset" in preset["params"]:
        rmax = max(1, n_periods - 2)
        kwargs["reset_cycle"] = st.slider("RD 在第几个时钟周期内拉低", 1, rmax, min(2, rmax), key="rc_%d" % rmax)

res = preset["sim"](n_periods=n_periods, **kwargs)

st.markdown("## §2 波形")
st.caption("淡色竖虚线 = CP 的上升沿（采样时刻）；Q 只在这些时刻更新，其余时间保持不变。")

rows = res["rows"]
fig = make_subplots(rows=len(rows), cols=1, shared_xaxes=True, vertical_spacing=0.08)

for xe in res["edges"]:
    fig.add_shape(
        type="line",
        x0=xe,
        x1=xe,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color=C_GRID, width=1, dash="dot"),
    )

for i, name in enumerate(rows, start=1):
    fig.add_trace(
        go.Scatter(
            x=res["t"],
            y=res["signals"][name],
            mode="lines",
            line_shape="hv",
            line=dict(color=ROW_COLOR.get(name, C_Q), width=2.2),
            name=name,
            showlegend=False,
            hovertemplate=name + ": %{y}<extra></extra>",
        ),
        row=i,
        col=1,
    )
    fig.update_yaxes(
        row=i,
        col=1,
        tickvals=[0, 1],
        tickfont=dict(size=10),
        title_text=name,
        range=[-0.4, 1.5],
    )

fig.update_xaxes(row=len(rows), col=1, title_text="时间（单位：时钟周期）", dtick=1, range=[0, n_periods])

styled = ui.style_fig(fig, height=120 * len(rows) + 110)
show_fig(styled if styled is not None else fig)

st.markdown("## §3 逐拍状态（自动生成）")
st.markdown(res["table"])

st.markdown("## §4 🎯 842 考点速记")

with st.expander("① 画波形题的三步套路", expanded=True):
    st.markdown(
        """
1. **先画 CP**，在每个有效边沿（本题是上升沿）画一条淡色竖线，标出“采样时刻”。
2. **写出次态方程**：D 触发器 Q(n+1) = D；JK 触发器 Q(n+1) = J·Q′ + K′·Q（Q′ 表示取反）；T 触发器 Q(n+1) = T ⊕ Q。
3. **只在采样时刻更新**：在边沿那一“瞬”把 Q 换成新值，其余时间 Q 一动不动 —— 这就是边沿触发与电平触发的分水岭。
4. 最后**回头验算**：Q2 的频率是不是 CP 的 1/4？移位寄存器是不是每拍只挪一格？
"""
    )

with st.expander("② 异步计数器为什么能分频"):
    st.markdown(
        """
每一级都是 T 触发器（D 接自己的 Q 的反，或者 JK 都接 1），每来一个时钟沿就翻转一次，
而“翻转一次”就意味着频率减半：

* 1 级 → 二分频
* 2 级串联 → 四分频
* n 级串联 → 2 的 n 次方分频

842 常考的写法是：**后级用前级的下降沿触发**（或者把前级的 Q 的反接到后级）。这样计数才连续。
"""
    )

with st.expander("③ 同步 vs 异步：一处关键区别"):
    st.markdown(
        """
| | 同步计数器 | 异步计数器 |
| --- | --- | --- |
| 时钟 | 所有触发器共用 CP | 前一级的输出就是后一级的时钟 |
| 翻转时刻 | 全部在同一个 CP 边沿 | 逐级触发（实际器件有传输延迟） |
| 画波形 | 所有 Q 的跳变对齐 CP 边沿 | 后级跳变对齐前级的跳变 |
| 优点 | 速度快、没有中间态毛刺 | 电路简单 |
| 常考 | 状态方程、状态表 | 分频比、触发沿的选择 |

本页面里 ① 和 ② 就是这两类的对照，来回切换看一遍就懂了。
"""
    )

with st.expander("④ 异步复位为什么优先级最高"):
    st.markdown(
        """
异步复位的“异步”是指：**它不必等 CP 边沿**。RD 一拉低，Q 立刻清零；
RD 拉高以后 Q 从 0 重新开始，但要**等下一个 CP 有效边沿**才会继续变化。

* 画波形时：RD 的低电平可以“打断”在两个时钟沿之间，Q 要在那一刻立刻掉到 0；
* 优先级：异步复位 > 时钟边沿。如果 RD 和 CP 边沿同时有效，听 RD 的；
* 对比同步复位：同步复位要等 CP 边沿才生效，Q 不会在两个沿之间突然变。
"""
    )

with st.expander("⑤ 三个最容易扣分的点"):
    st.markdown(
        """
1. **把边沿触发器画成电平触发**：CP 高电平期间 Q 跟着 D 变 —— 那是 D 锁存器，不是 D 触发器。
2. **忘了“同时更新”**：移位寄存器里 Q2 取的是这一拍**之前**的 Q1，不能先更新 Q1 再拿新的 Q1 去算 Q2。
3. **异步复位后忘了从 0 重新数**：复位解除后，Q 的翻转节奏接着下一个 CP 边沿算，不能顺着复位前的状态继续。
"""
    )
