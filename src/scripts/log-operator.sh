#!/bin/bash
TODAY=$(date +%Y%m%d)

if [[ -z ${INCLUDE_TODAY} ]]; then
  SEARCH=($(ls -A ${SEARCH_TARGET} | grep -v ${TODAY}))
else
  SEARCH=($(ls -A ${SEARCH_TARGET}))
fi

rm -rf /upload; mkdir /upload
for upload in "${SEARCH[@]}"; do
  echo "Copy ${upload} into /upload folder"
  cp ${upload} /upload/.
  if [[ -z ${REQUIRE_DELETE} ]]; then
    echo "Ignore remove ${upload}"
  else
    rm ${upload} || exit 1
    echo "${upload} deleted"
  fi
done

UPLOAD=($(ls -A /upload/*.*))

for upload in "${UPLOAD[@]}"; do
  echo "Upload ${upload} to ${UPLOAD_URL}/${upload##*/}"

  if [[ -z ${UPLOAD_TO_GCS} ]]; then
    echo "Ignore ${upload} to upload to gcs"
  else
    gsutil cp ${upload} ${UPLOAD_URL}/${upload##*/} || exit 1
    echo "Upload ${upload} to ${UPLOAD_URL}/${upload##*/} Success..."
  fi
done

rm -rf /upload

echo "Done ..."
