"""digital-lab 首页：项目门户。"""

import streamlit as st

import ui

ui.hero(
    "digital-lab",
    "数字电路 · 交互式实验室 —— 对着浙江大学 842《信号系统与数字电路》考纲搭建",
    ["ZJU 842", "DIGITAL CIRCUITS", "MACHINE-AIDED LEARNING"],
)

st.write("")

c1, c2, c3, c4 = st.columns(4)
with c1:
    with st.container(border=True):
        st.metric("交互模块", "2", help="另有 §0 电路分析速览作为地基")
with c2:
    with st.container(border=True):
        st.metric("覆盖主线", "2 条", help="数字电路主线 + RLC 系统地基")
with c3:
    with st.container(border=True):
        st.metric("技术栈", "Plotly", help="numpy + plotly + streamlit，不装额外依赖")
with c4:
    with st.container(border=True):
        st.metric("状态", "已上线", help="https://zju-digital-lab.streamlit.app")

st.write("")
st.markdown("## §1 交互模块")
ui.rule_caption("点击卡片进入 · 每个模块都能实时改参数、立刻看结果")

MODULES = [
    (
        "views/0_电路分析速览.py",
        "⚡ 电路分析速览",
        "RLC ↔ 系统函数 ↔ 零极点：842 不单独考电路分析，但它是信号部分的地基",
    ),
    (
        "views/1_卡诺图化简器.py",
        "🎯 卡诺图化简器",
        "填真值表（含无关项），自动给出最简与或式，并把每个圈画在图上",
    ),
    (
        "views/2_触发器波形.py",
        "🔀 触发器波形",
        "D / JK / T 三种触发器，边沿触发与电平触发对比，逐拍推算 Q",
    ),
]

cols = st.columns(2)
for i, (page, title, desc) in enumerate(MODULES):
    with cols[i % 2]:
        with st.container(border=True):
            st.page_link(page, label=title)
            st.caption(desc)

st.write("")
st.markdown("## §2 路线图")
ui.rule_caption("按 842 真题出现频率分三期 · ✅ 表示已完成")

st.markdown(
    """
| 期次 | 模块 | 状态 |
| --- | --- | --- |
| P0 · 必考 | ① 卡诺图化简器 | ✅ 已完成 |
| P0 · 必考 | ② 触发器波形 | ✅ 已完成 |
| P0 · 必考 | ③ 时序波形图工具 | 🚧 下一步 |
| P0 · 必考 | ④ 计数器 / 移位寄存器 | 计划中 |
| P0 · 必考 | ⑤ 555 定时器 | 计划中 |
| P1 · 常考 | ⑥ 数据选择器 / 译码器实现逻辑函数 | 计划中 |
| P1 · 常考 | ⑦ 控制器设计（浙大每年必考） | 计划中 |
| P1 · 常考 | ⑧ 竞争冒险判别与消除 | 计划中 |
| P1 · 常考 | ⑨ 门电路特性 TTL / CMOS | 计划中 |
| P2 · 拓展 | ⑩ 存储器容量计算与扩展 | 计划中 |
| P2 · 拓展 | ⑪ ADC / DAC | 计划中 |
| P2 · 拓展 | ⑫ RLC 电路桥梁模块 | 计划中 |
"""
)

st.write("")
st.markdown("## §3 相关项目")
with st.container(border=True):
    st.markdown("**📡 signal-lab · 信号与系统交互式实验室**")
    st.markdown("842 的另一半（信号与系统），已经上线：")
    st.markdown("- 🔗 在线体验：https://zju-signal-lab.streamlit.app")
    st.markdown("- 📦 源码仓库：https://github.com/Palpitate-kkkk/signal-lab")
with st.container(border=True):
    st.markdown("**🔌 digital-lab · 本项目**")
    st.markdown("- 🔗 在线体验：https://zju-digital-lab.streamlit.app")
    st.markdown("- 📦 源码仓库：https://github.com/Palpitate-kkkk/digital-lab")

st.write("")
ui.rule_caption("Made with Streamlit · numpy · Plotly · 献给 842")
