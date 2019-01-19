#!/bin/bash
TODAY=$(date +%Y%m%d)

if [[ -z ${INCLUDE_TODAY} ]]; then
  SEARCH=($(ls -A ${SEARCH_TARGET} | grep -v ${TODAY}))
else
  SEARCH=($(ls -A ${SEARCH_TARGET}))
fi

for log in "${SEARCH[@]}"; do
  echo "Copy ${log} to ${UPLOAD_URL}/${log##*/}"

  if [[ -z ${UPLOAD_TO_GCS} ]]; then
    echo "Ignore ${log} to upload to gcs"
  else
    gsutil cp ${log} ${UPLOAD_URL}/${log##*/} || exit 0
    echo "Upload ${log} to ${UPLOAD_URL}/${log##*/} Success..."
  fi

  if [[ -z ${REQUIRE_DELETE} ]]; then
    echo "Ignore removing ${log}"
  else
    rm ${log} || exit 1
    echo "${log} deleted"
  fi
done

echo "Done..."
