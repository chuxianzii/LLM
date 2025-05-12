import asyncio
import os
from mcp import Tool

# 使用异步的OpenAI客户端
from openai import AsyncOpenAI

# 使用dataclasss来定义数据类
from dataclasses import dataclass, field

from openai.types import FunctionDefinition
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
import dotenv
from pydantic import BaseModel
from rich import print as rprint

from augmented.utils import pretty

dotenv.load_dotenv()  # 加载环境变量


@dataclass
class AsyncChat:
    model: str
    messages: list[ChatCompletionMessageParam] = field(default_factory=list)
    tools: list[Tool] = field(default_factory=list)

    system_promprt: str = "You are a helpful assistant."
    context: str = ""

    llm: AsyncOpenAI = field(init=False)

    # 初始化之后自动被调用
    def __post_init__(self):
        # 创建异步的OpenAI客户端
        self.llm = AsyncOpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url=os.environ.get("DEEPSEEK_BASE_URL"),
        )
