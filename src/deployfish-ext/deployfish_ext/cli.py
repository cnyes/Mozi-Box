from deployfish.cli import cli
from deployfish.aws.ecs import Service
from deployfish_ext.core import BatchTask, CrontabJobs, LoggingHelper
from deployfish_ext.config import ConfigHelper

import click


@cli.group(short_help="Provides extends future for cnyes ecs deployment.")
def ext():
    """
    Provides extends future for cnyes ecs deployment.
    """


@ext.command(
    'batch_task', short_help="Run one-off task with service helper tasks.")
@click.pass_context
@click.argument('service_name')
@click.argument('task_family')
@click.argument('command')
@click.option(
    '--wait/--no-wait',
    default=False,
    help="Don't exit until ecs task is stopped.")
def batch_task(ctx, service_name, task_family, command, wait):
    """
    Run one-off task with COMMAND on service helper tasks FAMILY_NAME.
    """
    ConfigHelper.init(ctx)
    config = ConfigHelper.get_helper_tasks(service_name, task_family)
    cluster_name = ConfigHelper.get_cluster_name(service_name)
    batch = BatchTask(yml=config)
    LoggingHelper.print_info(batch.get_task_def_diff())
    batch.createOrUpdate()
    batch.run(command=command, cluster_name=cluster_name, wait=wait)


@ext.command(
    'cron_sync',
    short_help="Create / update cron jobs list with cloudwatch event.")
@click.pass_context
@click.argument('cron_name')
def cron_sync(ctx, cron_name):
    """
    Create / update cron jobs list with cloudwatch event with CRON_NAME.
    """
    ConfigHelper.init(ctx)
    cron_config = ConfigHelper.get_cronjobs_config(cron_name)
    help_tasks_config = ConfigHelper.get_helper_tasks(cron_name)
    cluster_name = ConfigHelper.get_cluster_name(cron_name)
    CrontabJobs(
        cluster_name=cluster_name,
        yml_cron=cron_config,
        yml_help_tasks=help_tasks_config).sync()


@ext.command(
    'service_exists', short_help="Check ecs service is already exists.")
@click.pass_context
@click.argument('service_name')
def service_exists(ctx, service_name):
    """
    Check ecs service with SERVICE_NAME is already exists.
    """
    ConfigHelper.init(ctx)
    if Service(service_name, config=ConfigHelper.get_config()).exists():
        LoggingHelper.print_info_n_exit(
            "service {} is already exists.".format(service_name), 0)
    else:
        LoggingHelper.print_info_n_exit(
            "service {} is not exists.".format(service_name), 1)

@ext.command(
    'service_stable', short_help="Wait until ecs service is stable.")
@click.pass_context
@click.argument('service_name')
def service_stable(ctx, service_name):
    """
    Wait until ecs service SERVICE_NAME is stable.
    """
    ConfigHelper.init(ctx)
    if Service(service_name, config=ConfigHelper.get_config()).wait_until_stable():
        LoggingHelper.print_info_n_exit(
            "service {} is stable.".format(service_name), 0)
    else:
        LoggingHelper.print_info_n_exit(
            "service {} is not stable.".format(service_name), 1)
