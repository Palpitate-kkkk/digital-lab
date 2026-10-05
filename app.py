import streamlit as st

from ui import inject_css

st.set_page_config(
    page_title="digital-lab · 数字电路交互式实验室",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

NAV = [
    st.Page("views/home.py", title="首页", icon="🏠", url_path="home", default=True),
    st.Page("views/0_电路分析速览.py", title="电路分析速览", icon="⚡", url_path="circuit-basics"),
    st.Page("views/1_卡诺图化简器.py", title="卡诺图化简器", icon="🎯", url_path="kmap"),
]

st.navigation(NAV).run()
