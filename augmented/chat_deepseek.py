import asyncio
import os

# mcp的工具
from mcp import Tool

# 使用异步的OpenAI客户端
from openai import AsyncOpenAI

# 使用dataclasss来定义数据类
from dataclasses import dataclass, field

# 定义可被openai 调用的函数
from openai.types import FunctionDefinition

# 定义聊天消息的参数、工具调用的参数
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
import dotenv
from pydantic import BaseModel
from rich import print as rprint

from utils import pretty

dotenv.load_dotenv()  # 加载环境变量


# 定义工具调用的参数
class ToolCallFunction(BaseModel):
    name: str = ""
    arguments: str = ""


# 定义一个返回后工具调用的类，因为只用到id,name和arguments
class ToolCall(BaseModel):
    id: str = ""
    function: ToolCallFunction = ToolCallFunction()


# 定义聊天返回的数据类型，content和tool_call调用列表
class ChatResponse(BaseModel):
    content: str = ""
    tool_calls: list[ToolCall] = []


@dataclass
class AsyncChat:
    model: str
    messages: list[ChatCompletionMessageParam] = field(default_factory=list)
    # 这里面的工具是mcp的工具，类型为Tool
    tools: list[Tool] = field(default_factory=list)

    # 系统的prompt
    system_prompt: str = "You are a helpful assistant."
    # 上下文信息
    context: str = ""

    llm: AsyncOpenAI = field(init=False)

    # 初始化之后自动被调用
    def __post_init__(self):
        # 创建异步的OpenAI客户端
        self.llm = AsyncOpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url=os.environ.get("DEEPSEEL_BASE_URL"),
        )
        # 添加系统prompt
        if self.system_prompt:
            self.messages.insert(0, {"role": "system", "content": self.system_prompt})
        # 添加上下文context，提供对话背景
        if self.context:
            self.messages.insert(1, {"role": "user", "content": self.context})

    # 将MCP的工具转换为OpenAI的工具定义
    def getToolsDefinition(self) -> list[ChatCompletionToolParam]:
        return [
            ChatCompletionToolParam(
                type="function",
                function=FunctionDefinition(
                    name=tool.name,
                    description=tool.description,
                    parameters=tool.parameters,
                ),
            )
            for tool in self.tools
        ]

    # 异步chat的实现——获取content和tool calls
    async def chat(self, prompt: str = "", print_llm_output: bool = True):
        # 输出一下格式
        pretty.log_title("CHAT")

        # 添加用户输入的prompt
        if prompt:
            self.messages.append({"role": "user", "content": prompt})

        print(self.messages)

        # 调用OpenAI的聊天接口，这里用到异步和流式处理
        chat_kwargs = {
            "model": self.model,
            "messages": self.messages,
            "stream": True,
        }
        if self.tools:
            chat_kwargs["tools"] = self.getToolsDefinition()

        streaming = await self.llm.chat.completions.create(**chat_kwargs)

        # 输出一下格式
        pretty.log_title("RESPONE")
        # 处理返回的流式数据，其中tool calls需要单独处理
        content = ""
        tool_calls: list[ToolCall] = []

        async for chunk in streaming:
            delta = chunk.choices[0].delta
            # 如果是 content
            if delta.content:
                content += delta.content or ""
                if print_llm_output:
                    print(delta.content, end="", flush=True)
            # 如果是工具调用
            if delta.tool_calls:
                for tool_call_chunk in delta.tool_calls:
                    # 收到一个tool_call，因为流式传输是片段，所以根据index来判断是否需要创建一个新的tool_call
                    if len(tool_calls) <= tool_call_chunk.index:
                        tool_calls.append(ToolCall())
                    current_tool_call = tool_calls[tool_call_chunk.index]
                    if tool_call_chunk.id:
                        current_tool_call.id = tool_call_chunk.id
                    if tool_call_chunk.function:
                        current_tool_call.function.name = (
                            tool_call_chunk.function.name or ""
                        )
                        current_tool_call.function.arguments = (
                            tool_call_chunk.function.arguments or ""
                        )

        # 维护一下messages
        self.messages.append(
            {
                "role": "assistant",
                "content": content,
                "tool_calls": [
                    {
                        "type": "function",
                        "id": tool_call.id,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in tool_calls
                ],
            }
        )

        # 返回获取的内容
        return ChatResponse(content=content, tool_calls=tool_calls)


async def example():
    llm = AsyncChat(
        model="deepseek-chat",
    )
    chat_response = await llm.chat(prompt="Hello")
    rprint(chat_response)


if __name__ == "__main__":
    asyncio.run(example())
