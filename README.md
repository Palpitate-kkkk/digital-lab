# digital-lab · 数字电路交互式实验室

🔗 **在线体验**：https://zju-digital-lab.streamlit.app （首次打开需唤醒约 30 秒）

📦 **源码仓库**：https://github.com/Palpitate-kkkk/digital-lab


对着浙江大学 842《信号系统与数字电路》考纲搭的交互式学习工具。

把数电里最难「看出来」的过程 —— 卡诺图化简、触发器翻转、时序波形、555 充放电 —— 做成可以拖参数、实时看结果的网页。

## 模块进度

| 模块 | 状态 |
|---|---|
| ⚡ 电路分析速览 | ✅ 已完成 |
| 🎯 卡诺图化简器 | 🚧 建设中 |
| 🔄 触发器波形仿真 | ⏳ 规划中 |
| 📊 时序波形图工具 | ⏳ 规划中 |
| 🔢 计数器 / 移位寄存器 | ⏳ 规划中 |
| ⏱️ 555 定时器 | ⏳ 规划中 |

## 技术栈

Streamlit · NumPy · SciPy · Plotly

## 本地运行

~~~bash
pip install -r requirements.txt
streamlit run app.py
~~~

## 目录结构

~~~
digital-lab/
├── app.py                  # 导航入口（st.navigation）
├── views/
│   ├── home.py             # 门户首页
│   └── 0_电路分析速览.py
├── .streamlit/config.toml  # 主题
└── requirements.txt
~~~
