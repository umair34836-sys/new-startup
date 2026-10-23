#!/usr/bin/env bash
# Agent tools for research and code navigation (installed outside the repo).
#   bash library/tools/setup-agent-tools.sh
# - Agent-Reach (Panniantong/Agent-Reach, MIT): read-only internet access for agents
#   (YouTube subtitles, Reddit, GitHub, web pages, X, ...). Never install the PyPI "agent-reach": it is a different project.
# - graft (NanoNets/Graft, now Trail-Code, MIT): builds a repo's context graph as linked markdown
#   (`graft build` is free/no key; `graft ask "<query>"` returns file:line). Telemetry turned off.
set -e
export PATH="$HOME/.local/bin:$PATH"
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip
agent-reach setup >/dev/null && agent-reach version
npm i -g @nanonets/graft@0.25.0
graft telemetry disable
