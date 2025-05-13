"""
modified from https://modelcontextprotocol.io/quickstart/client  in tab 'python'
"""

import asyncio
import shlex
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client

from rich import print as rprint

from dotenv import load_dotenv

from augmented.utils.info import PROJECT_ROOT_DIR
from augmented.utils.pretty import log_title

load_dotenv()


class MCPClient:
    def __init__(
        self,
        name: str,
        command: str,
        args: list[str],
        version: str = "0.0.1",
    ):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.name = name
        self.version = version
        self.command = command
        self.args = args
        self.tools: list[Tool] = []

    async def init(self):
        await self._connect_to_server()

    async def close(self):
        await self.exit_stack.aclose()

    def get_tools(self):
        return self.tools

    async def _connect_to_server(
        self,
    ):
        """
        Connect to an MCP server
        """
        print(f"[DEBUG] 启动 server: {self.command} {self.args}")
        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
        )
        print("[DEBUG] 准备进入 stdio_client")
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params),
        )
        print("[DEBUG] stdio_client 已连接")
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        print("[DEBUG] ClientSession 已建立，准备 initialize")
        await self.session.initialize()
        print("[DEBUG] initialize 完成，准备 list_tools")
        response = await self.session.list_tools()
        print("[DEBUG] list_tools 完成")
        self.tools = response.tools
        rprint("\nConnected to server with tools:", [tool.name for tool in self.tools])


async def example():
    print(f"[DEBUG] PROJECT_ROOT_DIR: {PROJECT_ROOT_DIR!r}")
    for mcp_name, cmd in [
        (
            "filesystem",
            [
                "npx",
                "-y",
                "@modelcontextprotocol/server-filesystem",
                str(PROJECT_ROOT_DIR),
            ],
        ),
        (
            "fetch",
            ["npx", "-y", "@modelcontextprotocol/server-fetch"],
        ),
    ]:
        log_title(mcp_name)
        command = cmd[0]
        args = cmd[1:]
        print(f"[DEBUG] command: {command}, args: {args}")
        mcp_client = MCPClient(
            name=mcp_name,
            command=command,
            args=args,
        )
        await mcp_client.init()
        tools = mcp_client.get_tools()
        rprint(tools)
        await mcp_client.close()


if __name__ == "__main__":
    asyncio.run(example())
