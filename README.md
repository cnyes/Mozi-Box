# Cnyes Mozi-Boxes

Cnyes Mozi-Boxes is a docker image, that provides a helper command collections to jenkins deployment jobs.

## Table of contents

* [built-in tools](#built-in-tools)
* [bitbucket-cli](#bitbucket-cli)
* [deployfish-ext](#deployfish-extension)
* [docker hub](https://hub.docker.com/r/anue/mozi-boxes)

## Built-in tools

* terraform 0.11.7
* jq
* git
* test-kitchen
* inspec
* gcloud
* kubectl

## Bitbucket cli

`bitbucket-cli bitbucket:patch-diff --help`

```
Usage:
  bitbucket:patch-diff <project> <id> (<id>)...

Arguments:
  project               bitbucket project where your PRs belong to.
  id                    PRs id arrays that you want to patch.

Options:
  -h, --help            Display this er message
  -q, --quiet           Do not output any message
  -V, --version         Display this application version
      --ansi            Force ANSI output
      --no-ansi         Disable ANSI output
  -n, --no-interaction  Do not ask any interactive question
      --env[=ENV]       The environment the command should run under
  -v|vv|vvv, --verbose  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug

er:
  This command is trying to fetch & patch diff with multiple PRs with bitbucket.
```

## Deployfish extension

### Command line reference

`deploy ext --help`

```
Usage: deploy ext [OPTIONS] COMMAND [ARGS]...

  Provides extends future for cnyes ecs deployment.

Options:
  --help  Show this message and exit.

Commands:
  batch_task      Run one-off task with service erer tasks.
  cron_sync       Create / update cron jobs list with cloudwatch event.
  service_exists  Check ecs service is already exists.
```

### Configuration (cronjobs)

`cronjobs` is a list of cron jobs based on service:

```
cronjobs:
  - name: foobar-prod
    target_role_arn: arn:aws:iam::474918040390:role/service-role/aws_events_ecs_role
    cron:
      cron_000: {type: ecs, cron: '*/10 * * * ? 2020', task: 'foobar-erer-prod', command: 'cron_000'}
      cron_001: {type: ecs, cron: '*/3 * * * ? 2020', task: 'foobar-erer-prod', command: 'cron_001'}
```

#### name

(String, Required) The name of cron job, and deployfish will failed if can not find match service name with `name`

#### target_role_arn

(String, Required) The aws resource arn that use for cloudwatch event target. CloudWatch Events needs permission to run tasks on your ECS Cluster. By continuing, you are allowing us to do so. ([learn more](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/iam-identity-based-access-control-cwe.html))

#### cron

`cron` is a list of cron job definition like so:

```
cron:
  cron_000: {type: ecs, cron: '*/10 * * * ? 2020', task: 'foobar-erer-prod', command: 'cron_000'}
  cron_001: {type: ecs, cron: '*/3 * * * ? 2020', task: 'foobar-erer-prod', command: 'cron_001'}
```

cron_000 (called rule_name) is stand for the part of cloudwatch events rule name deployfish will create.
real rule name combination rule : `cron-{name}-{rule_name}` (ex: cron-foobar-prod-cron-001)

##### type

(String, Required) is used to choose cloudwatch target type. currently only support for ecs.

##### cron

(String, Required) is stand cron-like schedule expression for cloudwatch events, different from linux crontab ([learn more](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions))

##### task

(String, Required) is reference for service helper task. if deployfish find the match helper task, it will use that helper task definition with command you specific to create new task definition for this cron job.

##### command

(String, Required) is reference for service helper task commands.

#### example configuration

```
services:
  - name: foobar-prod
    count: 1
    environment: prod
    cluster: foobar-prod-cluster
    family: foobar-prod
    network_mode: bridge
    containers:
      - name: web
        image: nginx:stable
        cpu: 10
        memory: 128
        ports:
          - "80:80"
        environment:
          - ENVIRONMENT=prod
          - SECRETS_BUCKET_NAME=my-secrets-bucket
    tasks:
      - family: foobar-helper-prod
        environment: prod
        network_mode: bridge
        containers:
          - name: app
            image: ubuntu:16.04
            cpu: 30
            memory: 128
            environment:
              - ENVIRONMENT=prod
              - SECRETS_BUCKET_NAME=my-secrets-bucket
        commands:
          test: sleep 60
          cron_000: date
          cron_001: ls -al /
cronjobs:
  - name: foobar-prod
    target_role_arn: arn:aws:iam::474918040390:role/service-role/aws_events_ecs_role
    cron:
      cron_000: {type: ecs, cron: '*/10 * * * ? 2020', task: 'foobar-helper-prod', command: 'cron_000'}
      cron_001: {type: ecs, cron: '*/3 * * * ? 2020', task: 'foobar-helper-prod', command: 'cron_001'}

```

#### iam example policy

based on https://github.com/caltechads/deployfish/issues/12

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "ecs:CreateService",
                "ecs:Describe*",
                "ecs:List*",
                "ecs:UpdateService",
                "ecs:DeleteService",
                "ecs:RegisterTaskDefinition",
                "ecs:RunTask",
                "ecs:StartTask",
                "ecs:StopTask",
                "ecs:SubmitTaskStateChange",
                "ecr:ListImages",
                "application-autoscaling:*",
                "elasticloadbalancing:Describe*",
                "cloudwatch:DescribeAlarms",
                "cloudwatch:DeleteAlarms",
                "cloudwatch:PutMetricAlarm",
                "events:ListRules",
                "events:ListTargetsByRule",
                "events:PutRule",
                "events:PutTargets",
                "events:DeleteRule",
                "events:RemoveTargets"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```
