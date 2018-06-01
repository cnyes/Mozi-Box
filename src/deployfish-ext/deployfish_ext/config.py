from deployfish.config import Config


class ConfigHelper(object):
    __config = None

    @staticmethod
    def get_service_config(service_name):
        if ConfigHelper.__config == None:
            raise RuntimeError(
                'ConfigHelper is not be initialized. please call ConfigHelper.init first.'
            )
        try:
            return ConfigHelper.__config.get_service(service_name)
        except KeyError:
            raise RuntimeError(
                "Can not find the service {} in config.".format(service_name))

    @staticmethod
    def get_helper_tasks(service_name, task_family=None):
        serviceConf = ConfigHelper.get_service_config(service_name)
        if 'tasks' in serviceConf:
            if task_family:
                for task in serviceConf['tasks']:
                    if task['family'] == task_family:
                        return task
                raise KeyError(
                    "Can not find the help task {} in config.".format(
                        task_family))
            else:
                return serviceConf['tasks']

        raise KeyError(
            "Can not find the tasks with service {} in config.".format(
                service_name))

    @staticmethod
    def get_cluster_name(service_name):
        try:
            return ConfigHelper.get_service_config(service_name)['cluster']
        except KeyError:
            raise RuntimeError(
                "Can not find the cluster with service {} in config.".format(
                    service_name))

    @staticmethod
    def get_cronjobs_config(name):
        try:
            return ConfigHelper.__config.get_category_item('cronjobs', name)
        except KeyError:
            raise RuntimeError(
                "Can not find the name {} in cronjobs config.".format(name))

    @staticmethod
    def init(ctx):
        ConfigHelper.__config = Config(
            filename=ctx.obj['CONFIG_FILE'],
            env_file=ctx.obj['ENV_FILE'],
            import_env=ctx.obj['IMPORT_ENV'],
            tfe_token=ctx.obj['TFE_TOKEN'])
