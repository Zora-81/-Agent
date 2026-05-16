# 智能会议纪要生成与分析Agent

## 功能
- 输入会议文本，自动生成：讨论要点、待办事项、风险点、总结
- 支持DeepSeek API（兼容OpenAI）
- 提供Streamlit Web界面

## 快速运行
1. 安装依赖：`pip install -r requirements.txt`
2. 在`.env`中填入`DEEPSEEK_API_KEY`
3. 运行：`streamlit run app.py`

## 证据生成指南（满足提交要求）
### 1. 账单截图
- 登录 [DeepSeek平台](https://platform.deepseek.com/) → 账单 → 截图近30天调用记录

### 2. 终端运行日志/工作流截图
- 在终端运行 `python agent.py` 或 `streamlit run app.py`，打印日志并截图
- 或使用录屏工具录制完整交互过程

### 3. GitHub项目链接/在线演示地址
- 将本项目上传到GitHub（记得忽略.env）
- 部署到Streamlit Cloud：https://streamlit.io/cloud （免费），获得公开链接

## 技术栈
- Python 3.9+
- Streamlit
- DeepSeek API
