#!/bin/bash
# Tools for the client portal (portal/): Android SDK for the TWA APK, and the owner-named design/agent repos.
#   bash library/tools/setup-portal-dev.sh          # everything (Android SDK ~1 GB download: on demand only)
#   bash library/tools/setup-portal-dev.sh repos    # only refresh ui-ux-pro-max + agency-agents copies
# Findings and licences: library/research/client-portal-tools.md
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
T=/home/user/tools
SDK="$T/android-sdk"
mkdir -p "$T/ext"

repos() {
  # nextlevelbuilder/ui-ux-pro-max-skill (MIT) -> .claude/skills/ui-ux-pro-max (already committed; this refreshes it).
  [ -d "$T/ext/ui-ux-pro-max-skill" ] || git clone -q --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git "$T/ext/ui-ux-pro-max-skill"
  # msitarzewski/agency-agents (MIT): a few personas copied to .claude/agents/agency-*.md (committed).
  [ -d "$T/ext/agency-agents" ] || git clone -q --depth 1 https://github.com/msitarzewski/agency-agents.git "$T/ext/agency-agents"
}

android() {
  # Java: the container image has OpenJDK 21 (checked 2026-10-29).
  command -v java >/dev/null || { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq openjdk-21-jdk-headless; }
  if [ ! -x "$SDK/cmdline-tools/latest/bin/sdkmanager" ]; then
    mkdir -p "$SDK/cmdline-tools" && cd "$SDK/cmdline-tools" &&
      curl -sSLo clt.zip https://dl.google.com/android/repository/commandlinetools-linux-9862592_latest.zip &&
      unzip -q clt.zip && rm clt.zip && mv cmdline-tools latest
  fi
  export ANDROID_HOME="$SDK"
  yes | "$SDK/cmdline-tools/latest/bin/sdkmanager" --licenses >/dev/null 2>&1
  "$SDK/cmdline-tools/latest/bin/sdkmanager" "platforms;android-35" "platforms;android-36" "build-tools;35.0.0" "platform-tools" >/dev/null
  echo "Android SDK ready in $SDK"
}

case "${1:-all}" in
  repos) repos ;;
  android) android ;;
  all) repos; android ;;
esac
