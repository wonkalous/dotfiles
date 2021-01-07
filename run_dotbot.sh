#!/usr/bin/env bash
# set -e

CONFIG_SUFFIX=".conf.yaml"
DOTBOT_DIR="dotbot"
DOTBOT_BIN="bin/dotbot"
BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "${BASEDIR}"
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" -c "default${CONFIG_SUFFIX}"
# set +e
