#!/bin/bash
# usage: tools/run_agent.sh <spec_name> <JavaClass> "<extra notes>"
cd "$(dirname "$0")/.." || exit 1
N=$1; C=$2; shift 2
mkdir -p build/agent_logs
PROMPT="Rebuild character spec '$N' (Java class $C). Confirmed reference: docs/ref/confirmed/$N.jpg. $*"
printf '%s' "$PROMPT" | claude -p --agent blockbench-artist --model opus --permission-mode acceptEdits \
  --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Bash(./gradlew:*),Bash(python3:*),Bash(ls:*),Bash(cat:*),Bash(mkdir:*),Bash(sips:*)" > "build/agent_logs/$N.log" 2>&1
echo "agent $N finished: $(tail -c 800 build/agent_logs/$N.log)"
