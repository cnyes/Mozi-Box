#!/usr/bin/env bash

"${COMPOSE_CMD[@]}" build "${CMD_NAME_BASE}"
"${COMPOSE_CMD[@]}" build "${CMD_NAME_DEV}"
