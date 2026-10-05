import numpy as np
import plotly.graph_objects as go
import streamlit as st

import ui

ui.hero(
    "电路分析速览",
    "两年前的课，用一页纸捡回来 —— 只捡「数字电路与信号系统真的会用到」的那些",
    ["PREREQUISITE", "§ 0", "REVIEW"],
)

st.info(
    "842 考纲里没有独立的电路分析，但 **RLC 电路会作为 LTI 系统的一种模型**出现在信号部分"
    "（考纲原话：「常系数线性微分、差分方程，零极点图，模拟框图及 RLC 电路等」）。"
    "而数电里的门电路延迟、施密特触发器、单稳态、时钟线上的振铃，根子也全在这门课上。"
)

st.markdown("## §1 一页纸要点")

with st.expander("§1.1　电路定律与参考方向（一切方程的地基）"):
    st.markdown(r"""
- **KCL**：任一节点，$\sum i = 0$（流入 = 流出）
- **KVL**：任一回路，$\sum u = 0$
- **关联参考方向**下，$P = ui > 0$ 表示吸收功率
- ⚠️ 考场上丢分最多的一步：**先标参考方向，再列方程**。方向错，全盘皆错。
""")

with st.expander("§1.2　等效变换与戴维南 / 诺顿（数电判断逻辑电平时也靠它）"):
    st.markdown(r"""
| 定理 | 内容 | 怎么求 |
|---|---|---|
| 戴维南 | 线性含源一端口 → 电压源 $U_{oc}$ 串联 $R_{eq}$ | $U_{oc}$ = 开路电压；$R_{eq}$ = 独立源置零后从端口看进去的等效电阻 |
| 诺顿 | 同上 → 电流源 $I_{sc}$ 并联 $R_{eq}$ | $I_{sc}$ = 短路电流，且 $U_{oc} = I_{sc}\cdot R_{eq}$ |

- 有受控源时，$R_{eq}$ 要用**加压求流法**或**开路短路法**
- 最大功率传输：$R_L = R_{eq}$ 时 $P_{max} = \dfrac{U_{oc}^2}{4R_{eq}}$
- 🔗 数电里的应用：TTL / CMOS 门的输出等效、扇出能力、上拉电阻取值，本质都是戴维南
""")

with st.expander("§1.3　一阶动态电路：RC / RL 与「三要素法」"):
    st.markdown(r"""
- 时间常数：RC 电路 $\tau = RC$，RL 电路 $\tau = \dfrac{L}{R}$
- **三要素法**：$f(t) = f(\infty) + \left[f(0^+) - f(\infty)\right]e^{-t/\tau}$
- 工程直觉：**$3\tau \approx 95\%$，$5\tau \approx 99\%$**，一般 5τ 后认为进入稳态
- 🔗 数电里的应用：门电路传输延迟、RC 延时电路、单稳态触发器脉宽 $T_w \approx 1.1RC$
""")

with st.expander("§1.4　二阶 RLC 电路与阻尼比（和 signal-lab 模块⑥是同一件事）"):
    st.markdown(r"""
- 串联 RLC：$\omega_n = \dfrac{1}{\sqrt{LC}}$，$\zeta = \dfrac{R}{2}\sqrt{\dfrac{C}{L}}$
- 特征方程 $s^2 + 2\zeta\omega_n s + \omega_n^2 = 0$，极点 $s = -\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2}$

| 阻尼比 | 极点 | 时域表现 |
|---|---|---|
| $\zeta > 1$ 过阻尼 | 两个负实极点 | 单调爬升，无过冲 |
| $\zeta = 1$ 临界 | 重实极点 | 最快且无过冲 |
| $\zeta < 1$ 欠阻尼 | 共轭复极点 | 衰减振荡、有超调 |
| $\zeta = 0$ 无阻尼 | 虚轴上 | 等幅振荡 |

- 🔗 **数电里同样会出现**：时钟线振铃（阻抗不匹配）、施密特触发器的回差、单稳态的暂态过程
""")

with st.expander("§1.5　相量法与正弦稳态、谐振（842 滤波器部分的底色）"):
    st.markdown(r"""
- 相量：$u(t) = U_m\cos(\omega t + \varphi) \;\to\; \dot{U} = U_m\angle\varphi$
- 阻抗 $Z = R + jX$：感抗 $j\omega L$，容抗 $\dfrac{1}{j\omega C}$
- 串联谐振：$\omega_0 = \dfrac{1}{\sqrt{LC}}$，品质因数 $Q = \dfrac{\omega_0 L}{R} = \dfrac{1}{\omega_0 C R}$
- 🔗 signal-lab 模块④⑦讲滤波器、模块⑦讲三大逼近 —— **谐振就是滤波器的极端情形**
""")

with st.expander("§1.6　s 域分析法：电路分析与信号系统的接缝（最该记的一条）"):
    st.markdown(r"""
- 元件 s 域阻抗：$R \to R$，$L \to sL$，$C \to \dfrac{1}{sC}$
- 对电路直接列 KCL / KVL，解出 $H(s) = \dfrac{\text{输出}}{\text{输入}}$，一步到位
- 从 $H(s)$ 出发的零极点、频率响应、稳定性 —— 就是 signal-lab 模块⑥干掉的事
- 🔗 这条路径 842 **会间接考**：给你一个 RLC 电路图，让你求系统函数、判断滤波类型
""")

st.markdown("## §2 一阶 RC 的一步充电")

c1, c2 = st.columns([1, 3])
with c1:
    R_k = st.slider("R (kΩ)", 1, 100, 10, 1)
    C_n = st.slider("C (nF)", 1, 1000, 100, 5)
    tau = R_k * C_n                      # kΩ × nF = µs
    st.metric("时间常数 τ", "{:.0f} µs".format(tau))
    st.caption("kΩ × nF = µs，这一步心算要熟")

t = np.linspace(0, 5 * tau, 600)
u = 1 - np.exp(-t / tau)

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=u, mode="lines", name="uC / U",
                         line=dict(color=ui.ACCENT, width=2.6)))
for k, txt in [(1, "63.2 %"), (3, "95 %")]:
    yk = 1 - np.exp(-k)
    fig.add_trace(go.Scatter(x=[k * tau], y=[yk], mode="markers",
                             showlegend=False, hoverinfo="skip",
                             marker=dict(size=10, color=ui.ACCENT_WARM)))
    fig.add_annotation(x=k * tau, y=yk, text="t = {}τ  {}".format(k, txt),
                       showarrow=False, xshift=14, yshift=-20,
                       xanchor="left", yanchor="top",
                       font=dict(color=ui.ACCENT_WARM, size=13))

ui.style_fig(fig, height=380, title="一阶 RC 阶跃响应", x="t (µs)", y="uC / U")
fig.update_yaxes(range=[0, 1.06])
with c2:
    st.plotly_chart(fig, width="stretch")

st.markdown("## §3 二阶 RLC 的阻尼比")


def second_order_step(t, wn, zeta):
    """H(s) = wn² / (s² + 2ζwn·s + wn²) 的阶跃响应（解析解）"""
    if zeta < 1:
        wd = wn * np.sqrt(1 - zeta ** 2)
        return 1 - np.exp(-zeta * wn * t) * (
            np.cos(wd * t) + zeta / np.sqrt(1 - zeta ** 2) * np.sin(wd * t))
    if np.isclose(zeta, 1):
        return 1 - np.exp(-wn * t) * (1 + wn * t)
    r = np.sqrt(zeta ** 2 - 1)
    a, b = wn * (zeta + r), wn * (zeta - r)
    return 1 + wn ** 2 / (a - b) * (np.exp(-a * t) / a - np.exp(-b * t) / b)


WN = 1000.0
zeta = st.slider("阻尼比 ζ", 0.05, 3.00, 0.30, 0.05)

if zeta < 1:
    poles = [-zeta * WN + 1j * WN * np.sqrt(1 - zeta ** 2),
             -zeta * WN - 1j * WN * np.sqrt(1 - zeta ** 2)]
    mp = np.exp(-np.pi * zeta / np.sqrt(1 - zeta ** 2))
    mp_txt = "超调量 {:.1f} %".format(mp * 100)
else:
    r = WN * np.sqrt(zeta ** 2 - 1)
    poles = [-zeta * WN + r, -zeta * WN - r]
    mp_txt = "无过冲"

t2 = np.linspace(0, min(4 / (zeta * WN), 40 / WN), 800)
y = second_order_step(t2, WN, zeta)

colA, colB = st.columns([3, 2])

with colA:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t2 * 1e3, y=y, mode="lines", name="y(t)",
                              line=dict(color=ui.ACCENT, width=2.6)))
    fig2.add_hline(y=1.0, line_dash="dot", line_color="#94A3B8")
    ui.style_fig(fig2, height=360, title="阶跃响应（{}）".format(mp_txt), x="t (ms)", y="y(t)")
    st.plotly_chart(fig2, width="stretch")

with colB:
    fig3 = go.Figure()
    fig3.add_hline(y=0, line_color="#CBD5E1")
    fig3.add_vline(x=0, line_color="#CBD5E1")
    fig3.add_trace(go.Scatter(x=[p.real for p in poles], y=[p.imag for p in poles],
                              mode="markers", name="极点",
                              marker=dict(size=14, symbol="x", color=ui.ACCENT_WARM)))
    ui.style_fig(fig3, height=360, title="s 平面极点位置", x="σ", y="jω")
    fig3.update_xaxes(range=[-3.5 * WN, 0.6 * WN])
    fig3.update_yaxes(range=[-3.0 * WN, 3.0 * WN])
    st.plotly_chart(fig3, width="stretch")
    st.caption("ζ 越小 → 极点越贴近虚轴 → 振荡越久、超调越大；ζ 变大 → 极点退到负实轴 → 过阻尼。")

st.markdown("## §4 与 842 / 数电的对照")

st.markdown(r"""
| 电分里的概念 | 它在数电 / 842 里以什么面目出现 |
|---|---|
| 戴维南等效 | TTL / CMOS 门的输出等效电路、扇出、上拉电阻 |
| 一阶 RC、时间常数 τ | 门电路传输延迟、单稳态脉宽 $T_w \approx 1.1RC$、RC 延时电路 |
| 二阶 RLC、阻尼比 ζ | 时钟线振铃、施密特触发器回差、单稳态暂态过程 |
| 相量法、谐振 | 842 滤波器部分（signal-lab 模块④⑦）的物理底色 |
| s 域阻抗与 $H(s)$ | **信号部分会考**：给电路图求系统函数、判断滤波类型 |
""")

ui.rule_caption("digital-lab · §0 电路分析速览 —— 配 signal-lab 模块⑥ 一起看，效果最好。")
