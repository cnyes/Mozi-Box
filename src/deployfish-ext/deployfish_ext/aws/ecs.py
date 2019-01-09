from deployfish.aws.ecs import TaskDefinition as OriginTaskDefinition

import boto3


class TaskDefinition(OriginTaskDefinition):
    def __init__(self, task_definition_id=None, yml={}):
        super(TaskDefinition, self).__init__()
        self.ecs = boto3.client('ecs')
        if task_definition_id:
            self.from_aws(task_definition_id)
        if yml:
            self.from_yaml(yml)


class EcsHelper(object):
    __client = None

    @staticmethod
    def __init():
        if not EcsHelper.__client:
            EcsHelper.__client = boto3.client('ecs')

    @staticmethod
    def get_cluster_arn(cluster_name):
        EcsHelper.__init()
        response = EcsHelper.__client.describe_clusters(
            clusters=[cluster_name])

        if 'failures' in response:
            if len(response['failures']
                   ) == 1 and response['failures'][0]['reason'] == 'MISSING':
                raise RuntimeError(
                    "Can not find ecs cluster {}".format(cluster_name))

        return response['clusters'][0]['clusterArn']

    @staticmethod
    def service_exists(cluster_name, service_name):
        EcsHelper.__init()
        response = EcsHelper.__client.describe_services(
            cluster=cluster_name,
            services=[service_name])

        if 'failures' in response and len(response['failures']) >= 1:
            if response['failures'][0]['reason'] == 'MISSING':
                return False
            else:
                raise RuntimeError(
                    "unknown error happend - response :\n{}".format(response))
        elif response['services'][0]['status'] == 'INACTIVE':
            return False

        return True
