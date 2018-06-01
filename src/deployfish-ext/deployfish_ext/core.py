from deployfish_ext.aws.cloudwatch_event import EventRule, EventECSTarget, EventsHelper
from deployfish_ext.aws.ecs import TaskDefinition, EcsHelper

import boto3
import click
import difflib
import sys
import traceback


class CrontabJobs(object):
    def __init__(self, cluster_name, yml_cron, yml_help_tasks):
        self._rules = {}
        self._tasks = {}
        self._name_prefix = None
        self._cluster_arn = EcsHelper.get_cluster_arn(cluster_name)
        self._target_role_arn = None
        self.from_yaml(yml_cron=yml_cron, yml_help_tasks=yml_help_tasks)

    def __yml_validate(self, yml):
        allowed_list = ['ecs', 'batch']
        field_needs = ['cron', 'type', 'task', 'command']

        keys_present = set(yml.keys())
        keys_needs = set(field_needs)

        diff = list(keys_present.symmetric_difference(keys_needs))
        if len(diff) > 0:
            raise RuntimeError("missing fields {}".format(diff))

        if yml['type'] not in allowed_list:
            raise ValueError("type {} is not in {}".format(
                yml['type'], allowed_list))

        if yml['task'] not in self._tasks:
            raise ValueError("task {} can not find in help tasks".format(
                yml['task']))

        task = self._tasks[yml['task']]
        if 'commands' not in task or yml['command'] not in task['commands']:
            raise ValueError("command {} can not find in help tasks".format(
                yml['command']))

    def __get_need_delete_rules(self, active_rules, desired_rules):
        set_active_rules = set(active_rules)
        set_desired_rules = set(desired_rules)
        return list(set_active_rules.difference(set_desired_rules))

    def from_yaml(self, yml_cron, yml_help_tasks):
        if 'target_role_arn' not in yml_cron:
            raise ValueError("target_role_arn is need for cronjobs config.")
        else:
            self._target_role_arn = yml_cron['target_role_arn']

        for task in yml_help_tasks:
            self._tasks[task['family']] = task

        self._name_prefix = "cron-{}".format(yml_cron['name'])
        for cron_name, propertyDict in yml_cron['cron'].items():
            self.__yml_validate(propertyDict)

            rule_name = "{}-{}".format(self._name_prefix, cron_name).replace(
                '_', '-')

            self._rules[rule_name] = {
                'rule':
                EventRule(name=rule_name, cron=propertyDict['cron']),
                'target_id':
                "{}-target".format(self._name_prefix).replace('_', '-')
            }

            yml_task = self._tasks[propertyDict['task']]
            yml_task['family'] = rule_name

            yml_task['containers'][0]['command'] = yml_task['commands'][
                propertyDict['command']]
            self._rules[rule_name]['task_def'] = BatchTask(yml_task)

    def sync(self):
        try:
            click.secho('Begin to sync.\n', fg='cyan')

            click.secho('Begin to prepare task : ', nl=False)
            rules_delete = self.__get_need_delete_rules(
                active_rules=EventsHelper.get_active_rule_list_names(
                    self._name_prefix),
                desired_rules=self._rules.keys())
            click.secho('success', fg='green')

            click.secho('\nBegin to update rules.', fg='cyan')
            click.secho(
                'Rules that need to create or update : {}'.format(
                    self._rules.keys()),
                fg='cyan')
            click.secho(
                'Rules that need to deleted : {}'.format(rules_delete),
                fg='cyan')
            click.secho('')

            for rule_name, rule in self._rules.items():
                msg_prefix = 'Rule [ {} ] '.format(rule_name)
                click.secho(msg_prefix, nl=False)
                rule['task_def'].print_task_def_diff()
                click.secho(msg_prefix, nl=False)
                rule['task_def'].createOrUpdate()

                click.secho(msg_prefix + 'begin to sync : ', nl=False)
                rule['rule'].createOrUpdate()
                EventECSTarget(rule['target_id'], self._cluster_arn,
                               rule['task_def'].definition_arn,
                               self._target_role_arn).createOrUpdate(rule_name)
                click.secho('success', fg='green')
                click.secho('')

            for rule_name in rules_delete:
                click.secho(
                    'Rule [ {} ] begin to delete : '.format(rule_name),
                    nl=False)
                EventsHelper.delete_rule(rule_name)
                click.secho('success', fg='green')
        except:
            click.secho('error', fg='red')
            click.secho('\nUnexpected error : ')
            print traceback.print_exc()


class BatchTask(object):
    def __init__(self, yml={}):
        self.ecs = boto3.client('ecs')
        self.commands = {}
        self.__extra_commands(yml)
        yml['family'] = "{}-{}".format('batch-task', yml['family']).replace(
            '_', '-')
        self.desired_task_definition = TaskDefinition(yml=yml)
        self.active_task_definition = None

    @property
    def definition_arn(self):
        if self.active_task_definition:
            return self.active_task_definition.arn
        else:
            return None

    def __extra_commands(self, yml):
        if 'commands' in yml:
            for key, value in yml['commands'].items():
                self.commands[key] = value.split()

    def from_aws(self, task_definition_id):
        try:
            if not self.active_task_definition:
                self.active_task_definition = TaskDefinition(
                    task_definition_id=task_definition_id)
        except KeyError:
            self.active_task_definition = None

    def print_task_def_diff(self):
        self.from_aws(self.desired_task_definition.family)
        expected = str(self.desired_task_definition).splitlines(1)
        actual = str(self.active_task_definition).splitlines(1)
        diff = difflib.unified_diff(expected, actual)

        click.secho(
            'Diff with desired task def & active task def : ', nl=False)
        diff = ''.join(diff)
        if diff:
            diff = '\n{}\n'.format(diff)
        else:
            diff = 'none'
        click.secho(diff, fg='cyan')

    def createOrUpdate(self):
        try:
            click.secho('Begin to create or update task def : ', nl=False)

            self.from_aws(self.desired_task_definition.family)
            if not str(self.active_task_definition) == str(
                    self.desired_task_definition):
                self.desired_task_definition.create()
                self.active_task_definition = self.desired_task_definition

            click.secho('success', fg='green')
        except:
            click.secho('error', fg='red')
            click.secho('\nUnexpected error: ')
            print traceback.print_exc()

    def run(self, command, cluster_name, wait):
        try:
            click.secho(
                'Begin to submit command {} with task {} : '.format(
                    command, self.active_task_definition.family),
                nl=False)

            if command not in self.commands:
                raise RuntimeError("Can not found command {} in task {}.",
                                   command, self.active_task_definition.family)

            response = self.ecs.run_task(
                cluster=cluster_name,
                taskDefinition=self.active_task_definition.arn,
                overrides={
                    'containerOverrides': [{
                        'name':
                        self.active_task_definition.containers[0].name,
                        'command':
                        self.commands[command]
                    }]
                })

            click.secho('success', fg='green')

            if response['failures']:
                raise RuntimeError(response['failures'][0]['reason'])

            if wait:
                click.secho('Begin to wait for complete : ', nl=False)
                waiter = self.ecs.get_waiter('tasks_stopped')
                waiter.wait(
                    cluster=cluster_name,
                    tasks=[response['tasks'][0]['taskArn']],
                    WaiterConfig={
                        'Delay': 10,
                        'MaxAttempts': 10
                    })
                click.secho('done', fg='green')
        except:
            click.secho('error', fg='red')
            click.secho('\nUnexpected error: ')
            print traceback.print_exc()
