#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export CLANG_MODULE_CACHE_PATH="${CLANG_MODULE_CACHE_PATH:-/private/tmp/swift-module-cache}"

exec /usr/bin/env swift "$SCRIPT_DIR/fix-claude-clipboard-image.swift" "$@"
