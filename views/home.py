import streamlit as st

import ui

ui.hero(
    "digital-lab",
    "数字电路 · 交互式实验室 —— 对着浙江大学 842《信号系统与数字电路》考纲搭建",
    ["ZJU 842", "SIGNAL & DIGITAL CIRCUITS", "MACHINE-AIDED LEARNING"],
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("交互模块", "1 / 12", help="规划 12 个，按考点优先级陆续补齐")
c2.metric("覆盖主线", "2 条", help="电路分析基础 · 数字电路")
c3.metric("技术栈", "Plotly", help="Streamlit + NumPy + SciPy + Plotly")
c4.metric("状态", "本地跑通", help="下一步：推上 GitHub 并部署上线")

st.markdown("## 模块导航")

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.markdown("#### ⚡ 电路分析速览")
        st.caption("戴维南等效 · 一阶暂态 · RLC 二阶阻尼 · 相量法与谐振 · s 域分析")
        st.page_link("views/0_电路分析速览.py", label="进入 →")
with right:
    with st.container(border=True):
        st.markdown("#### 🎯 卡诺图化简器")
        st.caption("点格子填 1 / 0 / ×，自动圈组，输出最简与或式与最小项编号")
        st.caption("🚧 下一步开工")

st.markdown("## 路线图")

st.markdown("""
| 优先级 | 模块 | 对应考点 |
|---|---|---|
| P0 | 卡诺图化简器 | 逻辑函数化简（年年考） |
| P0 | 触发器波形仿真 | SR / D / JK / T 特性方程与波形 |
| P0 | 时序波形图工具 | 组合 + 时序电路的画波形题 |
| P0 | 计数器 / 移位寄存器 | 同步/异步计数、扭环、环形 |
| P0 | 555 定时器 | 多谐振荡、单稳态、施密特触发器 |
| P1 | 数据选择器实现逻辑函数 | 「用 8 选 1 MUX 实现 F = Σm(...)」 |
| P1 | 控制器设计 | 浙大特色题，每年一道 |
| P1 | 竞争冒险判别 | 卡诺图相切圈 → 加冗余项 |
| P1 | TTL / CMOS 门电路特性 | 电压传输特性、噪声容限、扇出 |
| P2 | 存储器扩展 · ADC/DAC · RLC 桥梁 | 容量计算、量化误差、系统函数 |
""")

st.markdown("## 相关项目")
st.markdown(
    "- 📡 **signal-lab** · 信号与系统交互式实验室 —— "
    "[zju-signal-lab.streamlit.app](https://zju-signal-lab.streamlit.app)"
)
st.markdown(
    "- 📦 本仓库源码 —— [github.com/Palpitate-kkkk/digital-lab]"
    "(https://github.com/Palpitate-kkkk/digital-lab)（部署后生效）"
)

ui.rule_caption(
    "digital-lab · 与 signal-lab 同构（views/ + st.navigation）：一门课一个库，互为对照。"
)
