from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()  # 加载环境变量

# 可以直接明文写key和url，也可以通过设置全局系统变量来设置
# 但我这里选择使用python-dotenv，通过加载.env文件来设置 key和url
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEL_BASE_URL")
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "hello"},
    ],
    stream=True,
)

# 遍历流式响应的数据块
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)  # 实时输出内容
