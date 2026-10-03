"""
digital-lab · 统一视觉层
所有页面的字体、配色、图表模板都从这里出，保证「一本书」的观感。
配色：工科冷调深蓝 + 纯白底，只保留一处克制强调色。
"""
import streamlit as st

INK = "#12263A"          # 正文：近黑蓝
NAVY = "#1E3A5F"         # 主色：深蓝
ACCENT = "#3B6EA5"       # 图线主色：中性蓝
ACCENT_WARM = "#B0413E"  # 仅用于关键标记点（克制使用）
STEEL = "#8A9BAA"
LINE = "#E4E9EF"

CSS = """
<style>
html, body, [class*="css"] {
    font-family: -apple-system, "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}
.stApp { background: #FFFFFF; }

/* 标题：衬线体，教材观感 */
h1, h2, h3, h4 {
    font-family: Georgia, "Songti SC", "Times New Roman", serif !important;
    color: #1E3A5F;
    letter-spacing: .2px;
}
h1 { font-weight: 600; }
h2 {
    font-weight: 600;
    border-bottom: 1px solid #E4E9EF;
    padding-bottom: .35rem;
    margin-top: 1.9rem;
}
h3, h4 { font-weight: 600; color: #2C5580; }

/* 正文呼吸感 */
p, li { line-height: 1.85; }
[data-testid="stMarkdownContainer"] { color: #22374D; }

/* 链接：低调的下划虚线 */
[data-testid="stMarkdownContainer"] a {
    color: #2F5D8C;
    text-decoration: none;
    border-bottom: 1px dotted #A9BED4;
}

/* 表格：冷灰线、表头深蓝衬线 */
[data-testid="stMarkdownContainer"] table { border-collapse: collapse; width: 100%; }
[data-testid="stMarkdownContainer"] th {
    color: #1E3A5F;
    font-family: Georgia, "Songti SC", serif;
    border-bottom: 1px solid #D9E1E9 !important;
}
[data-testid="stMarkdownContainer"] td { border-bottom: 1px solid #F1F4F7 !important; }

/* 侧边栏 */
[data-testid="stSidebar"] {
    background: #F7F9FB;
    border-right: 1px solid #E4E9EF;
}

/* 指标卡：白底 + 冷灰细边 + 极浅阴影 */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E4E9EF;
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 1px 2px rgba(18, 38, 58, .04);
}
[data-testid="stMetricLabel"] { letter-spacing: .3px; }

/* 折叠区：像教材的边注 */
[data-testid="stExpander"] {
    border: 1px solid #E4E9EF;
    border-radius: 10px;
    background: #FFFFFF;
}
[data-testid="stExpander"] summary { font-weight: 600; color: #1E3A5F; }

/* 分隔线 */
hr { border: none; border-top: 1px solid #E4E9EF; margin: 1.9rem 0; }

/* 提示框 */
[data-testid="stAlert"] { border-radius: 10px; }

/* 收起默认页脚 */
footer { visibility: hidden; }
</style>
"""


def inject_css():
    """在 app.py 调用一次，全站生效"""
    st.markdown(CSS, unsafe_allow_html=True)


def hero(title, subtitle, tags=None):
    """页面头区：大标题 + 一句话 + 一排小型大写标签"""
    tag_html = ""
    if tags:
        items = " &nbsp;<span style='color:#D3DBE3;'>·</span>&nbsp; ".join(
            "<span style=\"letter-spacing:.14em;font-size:.70rem;color:#8A9BAA;\">{}</span>".format(t)
            for t in tags
        )
        tag_html = "<div style='margin-top:1rem;'>{}</div>".format(items)
    st.markdown(
        "<div style='padding:1.2rem 0 .3rem 0;'>"
        "<div style=\"font-family: Georgia, 'Songti SC', serif; font-size:2.1rem;"
        "font-weight:600; color:#1E3A5F; line-height:1.25;\">{}</div>"
        "<div style='color:#6D8095; margin-top:.5rem; font-size:.95rem;'>{}</div>"
        "{}</div>".format(title, subtitle, tag_html),
        unsafe_allow_html=True,
    )


def rule_caption(text):
    """页脚风格的小字"""
    st.markdown(
        "<div style='color:#94A3B3; font-size:.78rem; margin-top:1.4rem;'>{}</div>".format(text),
        unsafe_allow_html=True,
    )


def style_fig(fig, height=380, title=None, x=None, y=None):
    """统一所有 Plotly 图的观感"""
    fig.update_layout(
        template="simple_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        colorway=[ACCENT, STEEL, NAVY, ACCENT_WARM],
        font=dict(family="Georgia, 'Songti SC', serif", size=13, color="#1E3A5F"),
        margin=dict(l=8, r=14, t=50 if title else 28, b=8),
        legend=dict(bgcolor="rgba(255,255,255,.92)", bordercolor=LINE, borderwidth=1),
        title=dict(text=title, font=dict(size=15, color="#1E3A5F")) if title else None,
    )
    fig.update_xaxes(title=x, gridcolor="#F0F4F8", zeroline=False, linecolor="#D6DEE7")
    fig.update_yaxes(title=y, gridcolor="#F0F4F8", zeroline=False, linecolor="#D6DEE7")
    return fig
