#!/usr/bin/env bash

set -eo pipefail
shopt -s extglob

function get_container_id {
    "${COMPOSE_CMD[@]}" ps -q "${1}"
}

export PARENT_DIR

EXEC_PATH="${BASH_SOURCE[0]}"
[ -L "${BASH_SOURCE[0]}" ] && EXEC_PATH="$(readlink "${BASH_SOURCE[0]}")"
PARENT_DIR="$(dirname "${EXEC_PATH}")"
PARENT_DIR="$(cd "${PARENT_DIR}" && cd ../../ && pwd)"

export CMD_NAME="cnyes_deployment_cli"
export CMD_NAME_RELEASE="${CMD_NAME}_release"
export TASK_SECTION="${1}"
export PROJECT_NAME="${PROJECT_NAME:-}"

export COMPOSE_CMD=("docker-compose")

if [[ ! -z "${PROJECT_NAME}" ]]; then
    COMPOSE_CMD+=("-p" "${PROJECT_NAME}")
fi

export COMPOSE_EXEC_CMD=("${COMPOSE_CMD[@]}" "exec")
export COMPOSE_RUN_CMD=("${COMPOSE_CMD[@]}" "run" "--rm")

echo "running task section - [ ${TASK_SECTION} ]."
SCRIPT_FOLDER="${PARENT_DIR}/builds/docker/scripts/${TASK_SECTION}"
if [[ ! -d "${SCRIPT_FOLDER}" ]]; then
    echo "task section folder is not exists. exit."
    exit 1
fi

cd "${SCRIPT_FOLDER}" || exit 1
for task in *.sh; do
  echo ""
  echo "running task ${task:0:-3} ..."
  echo ""
  # shellcheck disable=SC1090
  source "${task}"
  echo ""
done

exit 0
