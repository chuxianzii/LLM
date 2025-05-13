set shell := ["pwsh.exe", "-c"]
set dotenv-required
set dotenv-load

default: help

help:
    @echo "`just -l`"

run_pretty:
    python augmented/utils/pretty.py

run_chat_deepseek:
    python augmented/chat_deepseek.py