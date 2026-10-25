# Artemis (google/artemis): AI agent that uses an Android phone

Installed here on 2026-10-25 because the owner asked: "Install artemis github tool".

## Which "Artemis"
A WebSearch on 2026-10-25 found several GitHub repos named Artemis. All answered `git ls-remote` on 2026-10-25:
- google/artemis: AI agent that drives an Android phone. **This is the one installed.**
- CERT-Polska/Artemis: web vulnerability scanner.
- ls1intum/Artemis: interactive learning platform.
- QUVA-Lab/artemis: Python experiment tools.

If the owner meant another one, install that one instead.

## Facts
- **README** (raw.githubusercontent.com/google/artemis/HEAD/README.md, read 2026-10-25):
  - Purpose: "Let AI assistants and test suites use real phones like a human".
  - Platform: Android only.
  - Licence: Apache-2.0.
  - Python 3.12+.
  - Needs an Android device with USB debugging, or an emulator.
  - Has an MCP server for Claude Code, plus a CLI: `uv run artemis run "<task>" --profile flash|pro`.
  - Has a web UI on localhost:8000.
- **Stars:** 12,338 stars, 1,430 forks, per a news page (pasqualepillitteri.it/en/news/25427/google-artemis-open-source-ai-agent-android-en, via WebSearch 2026-10-25). These numbers are not checked on GitHub, because github.com pages return 403 here.
- **Install** (measured here 2026-10-25):
  - Commands: `git clone --depth 1` (HEAD 351ca842, Sep 28 2026), then `uv sync --frozen --no-dev`.
  - Took 19 s; `.venv` is 1.1 GB.
  - adb comes from apt (`adb`, version 1.0.41).
  - Lives at /home/user/tools/artemis. It is also in setup-all.sh heavy.
- **`artemis doctor`** (measured here 2026-10-25):
  - Python 3.13.16 OK, config OK (planner model gemini-3.8-flash), MCP host OK.
  - **API key missing**: GEMINI_API_KEY, OPENAI_API_KEY or ANTHROPIC_API_KEY is required. Model use is paid.
  - **No device found.**
- **No emulator here:** this container has no /dev/kvm (checked 2026-10-25), so an Android emulator would be far too slow to be practical. A real phone can't plug into the cloud box over USB.
- **Telemetry:** `posthog` is a dependency, and a telemetry module exists (artemis/telemetry/). The opt-out is not checked yet.
- **Start:** don't run `./start.sh` unattended. It prompts to write global MCP configs and rules into IDEs.

## To actually use it
1. Get a multimodal API key (Gemini from aistudio.google.com, or another provider), then run `artemis init`.
2. Connect a device. Either:
   - run Artemis on the owner's own PC with the phone on USB, or
   - reach the phone over network adb (`adb connect <ip>:5555`, Android 11+ wireless debugging).

   Remote network adb is untested here.
