#!/usr/bin/env bash
echo "Start vscode debugger!!!"
python3 -m debugpy --listen 0.0.0.0:5000 --wait-for-client ./test.py stop