#!/bin/bash

gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${GKE_ZONE} --project ${GKE_PROJECT} || exit 1
