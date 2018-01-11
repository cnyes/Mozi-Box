#!/usr/bin/env bash

TEST_APP_ID="$(get_container_id "${CMD_NAME}")"

"${COMPOSE_EXEC_CMD[@]}" "${CMD_NAME}" ./vendor/bin/phing full-build || ERROR="true"
docker cp "${TEST_APP_ID}":/srv/app/builds/reports "${PARENT_DIR}/builds"

if [[ "${ERROR}" == "true" ]]; then
    echo "code quality testing failed. exit."
    exit 1
else
    echo "code quality testing success."
    echo "report files is under ./builds/reports"
fi
