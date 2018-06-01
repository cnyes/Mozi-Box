#!/usr/bin/env bash

TEST_APP_ID="$(get_container_id "${CMD_NAME_DEV}")"

"${DOCKER_EXEC_CMD[@]}" -w /srv/app/src/bitbucket-cli "${TEST_APP_ID}" composer run-script ci:test || ERROR="true"
[[ ! -d "${PARENT_DIR}/builds/reports" ]] && mkdir -p "${PARENT_DIR}/builds/reports"
docker cp "${TEST_APP_ID}":/srv/app/builds/reports/bitbucket-cli "${PARENT_DIR}/builds/reports/"

if [[ "${ERROR}" == "true" ]]; then
    echo "[bitbucket-cli] code quality testing failed. exit."
    exit 1
else
    echo "[bitbucket-cli] code quality testing success."
    echo "[bitbucket-cli] report files is under ./builds/reports"
fi
