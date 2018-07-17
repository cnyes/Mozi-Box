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
            LoggingHelper.print_info('begin to sync.')

            LoggingHelper.print_exec_info('begin to prepare task')
            rules_delete = self.__get_need_delete_rules(
                active_rules=EventsHelper.get_active_rule_list_names(
                    self._name_prefix),
                desired_rules=self._rules.keys())
            LoggingHelper.print_exec_success()

            LoggingHelper.print_info('begin to update rules.')
            LoggingHelper.print_info(
                'rules that need to create or update : {}'.format(
                    self._rules.keys()))
            LoggingHelper.print_info(
                'rules that need to deleted : {}'.format(rules_delete))

            for rule_name, rule in self._rules.items():
                LoggingHelper.set_global_prefix(
                    'rule [ {} ]'.format(rule_name))

                LoggingHelper.print_info(rule['task_def'].get_task_def_diff())

                rule['task_def'].createOrUpdate()

                LoggingHelper.print_exec_info('begin to sync')
                rule['rule'].createOrUpdate()
                EventECSTarget(rule['target_id'], self._cluster_arn,
                               rule['task_def'].definition_arn,
                               self._target_role_arn).createOrUpdate(rule_name)
                LoggingHelper.print_exec_success()

            for rule_name in rules_delete:
                LoggingHelper.set_global_prefix(
                    'rule [ {} ]'.format(rule_name))
                LoggingHelper.print_exec_info('begin to delete')
                EventsHelper.delete_rule(rule_name)
                LoggingHelper.print_exec_success()
        except SystemExit:  # you must have this except in order to exit with right status code.
            raise
        except:
            LoggingHelper.print_exec_fail()


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

    def get_task_def_diff(self):
        self.from_aws(self.desired_task_definition.family)
        expected = str(self.desired_task_definition).splitlines(1)
        actual = str(self.active_task_definition).splitlines(1)
        diff = difflib.unified_diff(actual, expected)

        diff = ''.join(diff)
        if diff:
            diff = '\n{}'.format(diff)
        else:
            diff = 'None'

        return '{} : {}'.format('Diff with desired task def & active task def',
                                diff)

    def createOrUpdate(self):
        try:
            LoggingHelper.print_exec_info('begin to create or update task def')

            self.from_aws(self.desired_task_definition.family)
            if not str(self.active_task_definition) == str(
                    self.desired_task_definition):
                self.desired_task_definition.create()
                self.active_task_definition = self.desired_task_definition

            LoggingHelper.print_exec_success()
        except SystemExit:  # you must have this except in order to exit with right status code.
            raise
        except:
            LoggingHelper.print_exec_fail()

    def run(self, command, cluster_name, wait):
        try:
            LoggingHelper.print_exec_info(
                'begin to submit command {} with task {}'.format(
                    command, self.active_task_definition.family))

            if command not in self.commands:
                raise RuntimeError(
                    "Can not found command {} in task {}.".format(
                        command, self.active_task_definition.family))

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

            LoggingHelper.print_exec_success()

            ecs_task_arn = None
            if response['failures']:
                raise RuntimeError(response['failures'][0]['reason'])
            else:
                ecs_task_arn = response['tasks'][0]['taskArn']

            if wait:
                LoggingHelper.print_exec_info('begin to wait for complete')
                waiter = self.ecs.get_waiter('tasks_stopped')
                waiter.wait(
                    cluster=cluster_name,
                    tasks=[response['tasks'][0]['taskArn']],
                    WaiterConfig={
                        'Delay': 10,
                        'MaxAttempts': 10
                    })
                LoggingHelper.print_exec_success()

                if ecs_task_arn is not None:
                    LoggingHelper.print_exec_info("exec status of ext_task")
                    response = self.ecs.describe_tasks(
                        cluster=cluster_name, tasks=[ecs_task_arn])
                    if response['failures']:
                        raise RuntimeError(response['failures'][0]['reason'])
                    else:
                        container_info = response['tasks'][0]['containers'][0]
                        exit_code = container_info['exitCode']
                        if exit_code == 0:
                            LoggingHelper.print_exec_success()
                        else:
                            LoggingHelper.print_exec_fail(showStackTrace=False)
                else:
                    LoggingHelper.print_info('task arn is missing. wtf !!!???')
            else:
                LoggingHelper.print_info(
                    'will always return 0 when you do not wait.')

        except SystemExit:  # you must have this except in order to exit with right status code.
            raise
        except:
            LoggingHelper.print_exec_fail()


class LoggingHelper(object):
    SUCCESS = 'success'
    FAILED = 'failed'

    __global_prefix = None

    @staticmethod
    def set_global_prefix(prefix):
        LoggingHelper.__global_prefix = prefix

    @staticmethod
    def print_info(description, need_prefix=True):
        if need_prefix and LoggingHelper.__global_prefix is not None:
            description = "{} {}".format(LoggingHelper.__global_prefix,
                                         description)
        click.secho(description.title(), fg='cyan')

    @staticmethod
    def print_exec_info(task_description, need_prefix=True):
        if need_prefix and LoggingHelper.__global_prefix is not None:
            task_description = "{} {}".format(LoggingHelper.__global_prefix,
                                              task_description)
        click.secho('{} : '.format(task_description).title(), nl=False)

    @staticmethod
    def __print_exec_status(status, showStackTrace):
        if status == LoggingHelper.SUCCESS:
            click.secho(LoggingHelper.SUCCESS, fg='green')
        else:
            click.secho(LoggingHelper.FAILED, fg='red')
            if showStackTrace:
                click.secho('\nUnexpected error: ')
                traceback.print_exc()
            sys.exit(1)

    @staticmethod
    def print_exec_success(showStackTrace=True):
        LoggingHelper.__print_exec_status(LoggingHelper.SUCCESS,
                                          showStackTrace)

    @staticmethod
    def print_exec_fail(showStackTrace=True):
        LoggingHelper.__print_exec_status(LoggingHelper.FAILED, showStackTrace)

    @staticmethod
    def print_info_n_exit(description, exit_code):
        LoggingHelper.print_info(description)
        sys.exit(exit_code)
