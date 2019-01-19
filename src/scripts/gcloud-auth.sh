#!/bin/bash

gcloud auth activate-service-account --key-file=/credential/credentials.json || exit 1
