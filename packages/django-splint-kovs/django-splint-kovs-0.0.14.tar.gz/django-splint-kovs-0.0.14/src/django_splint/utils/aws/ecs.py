from django.conf import settings

import boto3

SERVICE_NAME = 'ecs'
CONTAINER_DEFAULT_NAME = 'gunicorn'
COMMAND_NAME = 'run_task'

class AWSECSHandler:
    """AWS ECS service handler."""

    def __init__(self):
        """Constructor."""
        self.client = boto3.client(
            service_name=SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
        )
        self.container_default_name = CONTAINER_DEFAULT_NAME
        self.task_definition = settings.AWS_TASK_DEFINITION
        self.command_name = COMMAND_NAME

    def run_task(
            self, launch_type=settings.AWS_CLUSTER_LAUNCH,
            cluster=settings.AWS_CLUSTER, command=None,
            task_definition=settings.AWS_TASK_DEFINITION):
        """Run Task definition on ECS Cluster."""
        run_kwargs = {
            'cluster': cluster,
            'launchType': launch_type,
            'taskDefinition': self.task_definition,
        }
        if command:
            command = command.split() if isinstance(command, str) else command
            run_kwargs['overrides'] = {
                'containerOverrides': [
                    {
                        'name': self.container_default_name,
                        'command': command,
                    }
                ]
            }
        return self.client.run_task(**run_kwargs)