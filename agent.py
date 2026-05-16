import os
from openai import OpenAI

# 初始化DeepSeek客户端（兼容OpenAI接口）
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 从环境变量读取
    base_url="https://api.deepseek.com"
)

def call_llm(prompt: str, model: str = "deepseek-chat") -> str:
    """调用DeepSeek API生成内容"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的会议分析助手，擅长结构化输出。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API调用出错：{e}"

def meeting_agent(raw_text: str) -> dict:
    """会议分析Agent核心函数"""
    prompt = f"""
请根据以下会议内容，生成结构化的会议纪要。输出格式请严格按照下面的JSON结构：

{{
  "discussion_points": ["要点1", "要点2", ...],
  "action_items": [
    {{"task": "任务描述", "owner": "负责人（若未明确则填'待确认'）"}},
    ...
  ],
  "risks": ["风险点1", "风险点2", ...],
  "summary": "一句话总结"
}}

会议内容：
{raw_text}
"""
    response_text = call_llm(prompt)
    
    # 尝试解析JSON，若失败则返回原始文本
    import json
    try:
        # 提取可能的JSON部分
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end > start:
            json_str = response_text[start:end]
            return json.loads(json_str)
        else:
            return {"error": "输出格式不正确", "raw": response_text}
    except:
        return {"error": "JSON解析失败", "raw": response_text}

# 示例运行（测试用）
if __name__ == "__main__":
    test_text = "产品经理张三说：下周要发布新版本，后端李四需要完成API接口，前端王五准备页面。风险：服务器资源可能不足。"
    result = meeting_agent(test_text)
    print(result)