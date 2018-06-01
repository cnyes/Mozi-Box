# Cnyes Deployfish extension
---
cnyes custom extension for deployfish (https://github.com/caltechads/deployfish)
Help for cnyes aws ecs deployment.

## Prerequisite
* python 2.7
* deployfish >= 0.19.1
* make

## Main Feature
* check ecs service is already exists.
* run one-off task based on service help tasks.
* maintain cloudwatch events crontab rules.

## How to development.
```
$ pip install -e ./
```

## How to pack the package.
```
$ make dist
```
