import streamlit as st
import os
from dotenv import load_dotenv
from agent import meeting_agent
import json

# 加载环境变量
load_dotenv()

st.set_page_config(page_title="智能会议纪要Agent", layout="wide")
st.title("🎙️ 智能会议纪要生成与分析Agent")
st.markdown("输入会议文本，自动生成结构化纪要（讨论要点、待办事项、风险、总结）")

# 侧边栏API Key配置（可选，也可用.env文件）
with st.sidebar:
    st.header("⚙️ 配置")
    api_key = st.text_input("DeepSeek API Key", type="password", 
                            help="如果没有，去platform.deepseek.com注册获取")
    if api_key:
        os.environ["DEEPSEEK_API_KEY"] = api_key
    st.markdown("---")
    st.markdown("### 如何使用")
    st.markdown("1. 在下方输入会议文本\n2. 点击「生成纪要」\n3. 查看结构化结果")
    st.markdown("### 示例文本")
    if st.button("加载示例"):
        example = "产品经理：Q3目标是将用户留存提升10%。技术负责人：需要增加推荐算法迭代。运营：可以配合推送活动。风险：开发资源紧张。"
        st.session_state.input_text = example

# 主输入区
input_text = st.text_area("📝 会议文本（支持粘贴）", height=200, 
                          key="input_text", 
                          placeholder="例如：张三说：... 李四说：...")

if st.button("🚀 生成纪要", type="primary"):
    if not input_text.strip():
        st.warning("请输入会议文本")
    else:
        # 检查API Key
        if not os.getenv("DEEPSEEK_API_KEY") and not api_key:
            st.error("请先在侧边栏输入DeepSeek API Key")
        else:
            with st.spinner("AI正在分析中..."):
                result = meeting_agent(input_text)
            
            st.success("生成完成！")
            
            # 展示结果
            if "error" in result:
                st.error(f"解析出错: {result['error']}")
                st.text("原始返回:")
                st.code(result.get("raw", ""))
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📌 讨论要点")
                    for point in result.get("discussion_points", []):
                        st.write(f"- {point}")
                    
                    st.subheader("⚠️ 风险点")
                    for risk in result.get("risks", []):
                        st.write(f"- {risk}")
                
                with col2:
                    st.subheader("✅ 待办事项")
                    for item in result.get("action_items", []):
                        st.write(f"- **{item['task']}** (负责人: {item['owner']})")
                    
                    st.subheader("📄 总结")
                    st.write(result.get("summary", ""))
            
            # 显示原始JSON（用于日志截图）
            with st.expander("查看原始JSON输出"):
                st.json(result)