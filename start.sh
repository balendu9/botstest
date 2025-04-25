#!/bin/bash
# start.sh
nohup python bot.py &
uvicorn verifier:app --host 0.0.0.0 --port 10000

