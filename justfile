set shell := ["pwsh.exe", "-c"]
set dotenv-required
set dotenv-load

default: help

help:
    @echo "`just -l`"

run_pretty:
    python -m augmented.utils.pretty.py

run_chat_deepseek:
    python -m augmented.chat_deepseek.py

run_mcp_client:
    python -m augmented.mcp_client