import boto3


class EventRule(object):
    def __init__(self, name, cron):
        self.client = boto3.client('events')
        self._schedule_expression = None
        self._state = 'ENABLED'

        self.name = name
        self.description = name
        self.schedule_expression = cron

    @property
    def schedule_expression(self):
        return self._schedule_expression

    @schedule_expression.setter
    def schedule_expression(self, value):
        self._schedule_expression = "cron({})".format(value)

    @property
    def state(self):
        return self._state

    def createOrUpdate(self):
        self.client.put_rule(
            Name=self.name,
            ScheduleExpression=self.schedule_expression,
            State=self.state,
            Description=self.description)


class EventECSTarget(object):
    def __init__(self, target_id, ecs_cluster_arn, task_def_id, role_arn):
        self.client = boto3.client('events')
        self.target_id = target_id
        self.ecs_cluster_arn = ecs_cluster_arn
        self.task_def_id = task_def_id
        self.role_arn = role_arn

    def createOrUpdate(self, rule_name):
        target = {
            'Id': self.target_id,
            'Arn': self.ecs_cluster_arn,
            'RoleArn': self.role_arn,
            'EcsParameters': {
                'TaskDefinitionArn': self.task_def_id,
                'TaskCount': 1
            }
        }

        self.client.put_targets(Rule=rule_name, Targets=[target])


class EventsHelper(object):
    __client = None

    @staticmethod
    def __init():
        if not EventsHelper.__client:
            EventsHelper.__client = boto3.client('events')

    @staticmethod
    def __list_rules(rule_name_prefix, next_token=None, limit=100):
        if next_token:
            return EventsHelper.__client.list_rules(
                NamePrefix=rule_name_prefix, NextToken=next_token, Limit=limit)
        else:
            return EventsHelper.__client.list_rules(
                NamePrefix=rule_name_prefix, Limit=limit)

    @staticmethod
    def __get_names_from_list_rules_response(response):
        if response['Rules']:
            return [rule['Name'] for rule in response['Rules']]
        else:
            return []

    @staticmethod
    def get_active_rule_list_names(rule_name_prefix):
        EventsHelper.__init()
        names = []
        response = {'NextToken': None}

        while 'NextToken' in response:
            next_token = response['NextToken']
            response = EventsHelper.__list_rules(
                rule_name_prefix=rule_name_prefix, next_token=next_token)
            names += EventsHelper.__get_names_from_list_rules_response(
                response)

        return names

    @staticmethod
    def delete_rule(rule_name):
        EventsHelper.__init()
        response = EventsHelper.__client.list_targets_by_rule(Rule=rule_name)
        target_ids = [target['Id'] for target in response['Targets']]
        EventsHelper.__client.remove_targets(Rule=rule_name, Ids=target_ids)
        EventsHelper.__client.delete_rule(Name=rule_name)
