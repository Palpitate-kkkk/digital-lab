"""views/1_卡诺图化简器.py —— 填最小项，自动画圈 + 吐最简与或式"""
import plotly.graph_objects as go
import streamlit as st

import kmap
import ui

NAMES = "ABCDEF"
LOOP_COLORS = ["#B0413E", "#1E3A5F", "#2E6F6B", "#8A6A2F", "#5B5B8A"]

PRESETS = [
    ("例①", 3, "1,3,5,7", ""),
    ("例②", 4, "0,1,2,5,7", ""),
    ("例③", 4, "0,1,2,5,7", "3"),
    ("例④", 4, "0,2,4,6,8,10,12,14", ""),
]
PRESET_DESC = "例① 3变量 Σm(1,3,5,7)｜例② 4变量 Σm(0,1,2,5,7)｜例③ 例②+无关项 Σd(3)｜例④ 4变量 偶数最小项"


def rgba(color, alpha):
    h = color.lstrip("#")
    return "rgba({},{},{},{})".format(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def build_fig(n, ones, dcs, picked):
    rows, cols, cells = kmap.grid(n)
    R, C = len(rows), len(cols)
    rb, cb = kmap.layout(n)
    row_names, col_names = NAMES[:rb], NAMES[rb:rb + cb]

    fig = go.Figure()

    # 1) 格子：值 + 最小项编号
    for r in range(R):
        for c in range(C):
            m = cells[r][c]
            if m in ones:
                fill, edge, lab, col = "#E9F1F9", "#C6D7E8", "1", ui.NAVY
            elif m in dcs:
                fill, edge, lab, col = "#F3F5F7", "#D8DEE5", "×", ui.STEEL
            else:
                fill, edge, lab, col = "#FFFFFF", ui.LINE, "0", ui.STEEL
            fig.add_shape(type="rect", x0=c - 0.5, y0=r - 0.5, x1=c + 0.5, y1=r + 0.5,
                          line=dict(color=edge, width=1.2), fillcolor=fill, layer="below")
            fig.add_annotation(x=c, y=r, text=lab, showarrow=False,
                               xanchor="center", yanchor="middle",
                               font=dict(size=20, color=col))
            fig.add_annotation(x=c - 0.36, y=r - 0.32, text=str(m), showarrow=False,
                               xanchor="left", yanchor="middle",
                               font=dict(size=9.5, color=ui.STEEL))

    # 2) 圈：必须用该项的"完整覆盖"（含借来的 ×），否则圈会缺角
    for i, (spec, _cov) in enumerate(picked):
        color = LOOP_COLORS[i % len(LOOP_COLORS)]
        pad = 0.10 + 0.05 * i
        for (r0, r1, c0, c1) in kmap.group_rects(n, kmap.cover(spec)):
            fig.add_shape(type="rect",
                          x0=c0 - 0.5 + pad, y0=r0 - 0.5 + pad,
                          x1=c1 + 0.5 - pad, y1=r1 + 0.5 - pad,
                          line=dict(color=color, width=3),
                          fillcolor=rgba(color, 0.10), layer="above")

    ui.style_fig(fig, height=170 + 82 * R, title="{} 变量卡诺图".format(n),
                 x="列 {}".format(col_names), y="行 {}".format(row_names))
    fig.update_xaxes(showgrid=False, zeroline=False, ticks="", tickmode="array",
                     tickvals=list(range(C)),
                     ticktext=[format(v, "0{}b".format(cb)) for v in cols],
                     range=[-0.5, C - 0.5], tickfont=dict(size=13, color=ui.INK))
    fig.update_yaxes(showgrid=False, zeroline=False, ticks="", tickmode="array",
                     tickvals=list(range(R)),
                     ticktext=[format(v, "0{}b".format(rb)) for v in rows],
                     range=[R - 0.5, -0.5], tickfont=dict(size=13, color=ui.INK),
                     scaleanchor="x", scaleratio=1)
    return fig


ui.hero("卡诺图化简器", "填一组最小项 → 自动画圈 → 吐出最简与或式",
        ["ZJU 842", "§ 1", "K-MAP"])

for _k, _v in (("kmap_n", 4), ("kmap_ones", "0,1,2,5,7"), ("kmap_dcs", "")):
    if _k not in st.session_state:
        st.session_state[_k] = _v

st.markdown("## §1 输入")
_bcols = st.columns(len(PRESETS))
for _bc, (_lb, _pn, _po, _pd) in zip(_bcols, PRESETS):
    if _bc.button(_lb, key="preset_" + _lb):
        st.session_state["kmap_n"] = _pn
        st.session_state["kmap_ones"] = _po
        st.session_state["kmap_dcs"] = _pd
st.caption(PRESET_DESC)

c1, c2, c3 = st.columns([1, 2, 2])
with c1:
    n = st.radio("变量数", [2, 3, 4], key="kmap_n", horizontal=True)
with c2:
    ones_text = st.text_input("最小项 Σm（逗号分隔）", key="kmap_ones")
with c3:
    dcs_text = st.text_input("任意项 Σd（可空）", key="kmap_dcs")

ones, bad1 = kmap.parse_list(ones_text, n)
dcs, bad2 = kmap.parse_list(dcs_text, n)
dcs -= ones
if bad1 or bad2:
    st.warning("这些编号超出 {} 变量范围（0–{}），已忽略：{}".format(
        n, (1 << n) - 1, sorted(set(bad1 + bad2))))

picked = kmap.minimize(n, ones, dcs)
primes = kmap.prime_implicants(n, ones, dcs) if ones else []
cnt = {}
for _s, _c in primes:
    for _m in _c & ones:
        cnt[_m] = cnt.get(_m, 0) + 1
essential = {s for s, c in primes if any(cnt.get(m, 0) == 1 for m in c & ones)}

st.markdown("## §2 卡诺图")
st.plotly_chart(build_fig(n, ones, dcs, picked), width="stretch")
st.caption("每格左上角小字是最小项编号；× 是任意项。跨边界的圈会画成同色的两块，四角的圈会拆成四块。")

st.markdown("## §3 化简结果")
if not ones:
    st.info("一个最小项都没填 —— F = 0")
else:
    st.markdown("### F = {}".format(kmap.expr_str(picked)))
    st.caption("共 {} 个圈，每个圈对应一个乘积项".format(len(picked)))
    for i, (spec, cov) in enumerate(picked):
        color = LOOP_COLORS[i % len(LOOP_COLORS)]
        tags = []
        if spec in essential:
            tags.append("必要质蕴含项")
        borrowed = sorted(kmap.cover(spec) - ones)
        if borrowed:
            tags.append("借用了无关项 m{}".format(borrowed))
        st.markdown(
            "<span style='color:{}'>■</span> **{}** &nbsp;·&nbsp; 覆盖 m{} {}".format(
                color, kmap.term_str(spec), sorted(cov),
                "&nbsp;· " + "；".join(tags) if tags else ""),
            unsafe_allow_html=True)

st.markdown("## §4 842 考点速记")

with st.expander("① 为什么行列要按格雷码排"):
    st.markdown("""
- 格雷码相邻两项只差 **1 位**，所以卡诺图上"物理相邻"＝"逻辑上只差一个变量"＝ **可以合并消掉一位**。
- 这就是卡诺图能化简的全部底层逻辑：相邻 → 消元。2^k 个格子连成一片 → 消掉 k 个变量。
- 4 变量：行 `AB = 00 01 11 10`，列 `CD = 00 01 11 10`。注意是 `00 01 11 10`，不是 `00 01 10 11`。
""")

with st.expander("② 画圈的五条规矩"):
    st.markdown("""
1. 圈里格数必须是 **2 的幂**：1、2、4、8、16；
2. 圈要**尽量大**（越大消掉的变量越多），大到不能再大就停 —— 这叫**质蕴含项**；
3. 圈里只能有 1 和 ×，**绝对不能包含 0**；
4. 一个 1 可以被好几个圈共用（重复用不扣分）；
5. 允许跨上下边界、跨左右边界，**四个角算相邻**（四角圈合法）。
- 目标：用**最少的圈**把**所有的 1** 都圈到。
""")

with st.expander("③ 圈 ↔ 乘积项 怎么对应"):
    st.markdown("""
- **一个圈 = 一个乘积项**。
- 读法：看圈内**始终不变**的变量 —— 恒为 1 写原变量（`A`），恒为 0 写反变量（`A'`）；**变了的变量直接消掉**。
- 举例：`A'BD` 这个圈 = A 恒 0、B 恒 1、D 恒 1，C 在圈里 0/1 都出现过 → 消掉 C。
- 把每个圈的乘积项用 `+` 连起来，就是**最简与或式**（SOP）。
""")

with st.expander("④ 质蕴含项 vs 必要质蕴含项"):
    st.markdown("""
- **质蕴含项（PI）**：不能再往外扩大的圈。
- **必要质蕴含项（EPI）**：某个 1 **只有这一个圈**能盖住它 → 这个圈**必选**。
- 手算顺序：先把所有 EPI 圈上 → 划掉已覆盖的 1 → 剩下的 1 再挑圈（优先和已有圈共用格子）→ 直到全覆盖。
- 本工具用的是 Quine-McCluskey 精确算法（等价于"圈到底再挑项数最少的一组"），保证项数最少；等价最简式不止一个时，给的是其中一个。
""")

with st.expander("⑤ 无关项（×）怎么用"):
    st.markdown("""
- `×` 表示"这组输入不会出现，或者出现了也不关心输出"。
- 用法：**想用就用，不想用就当它 0**。用它的唯一目的是**把圈撑大** → 少消一个变量、少写一项。
- 禁忌：不能为了凑大圈而让圈包含 0；也不能为了用 × 反而把表达式搞复杂。
- 842 里"带无关项的化简"是高频题：**看到 × 先想能不能借力把圈撑大**。
""")

with st.expander("⑥ 842 常见题型 & 易错点"):
    st.markdown("""
**题型**
- 给最小项列表 → 求最简与或式（本工具直接给）；
- 给真值表 / 逻辑表达式 → 先填卡诺图再化简；
- 带无关项化简；
- 求最简**或与式**（POS）：改成对 **0** 画圈，先得 `F'` 的最简与或式，再整体取反（德摩根）；
- 与公式法对照，说明卡诺图为什么更省事。

**易错点（都是实打实的失分点）**
- 漏圈某个 1 → 结果少项；
- 圈里混进了 0；
- 圈里格数不是 2 的幂；
- 忘了跨边界 / 四角的那种圈；
- 读项时把"不变/可变"看错（**最常见**）：逐个变量核对它在圈内是否恒定。

> 卡诺图很少单独出大题，但它是组合逻辑设计的第 0 步；浙大那道年年出现的"控制器设计"题里也要用到。
""")

ui.rule_caption("kmap.py：Quine-McCluskey 精确求解 · 支持 2/3/4 变量与任意项")
