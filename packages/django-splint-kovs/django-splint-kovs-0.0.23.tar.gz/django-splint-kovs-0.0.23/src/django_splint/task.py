from django_splint.utils.aws.ecs import AWSECSHandler


class SplintTask(AWSECSHandler):

    def delay(self, *args):
        """Run task in AWS ECS."""
        return AWSECSHandler().run_task(
            command=f'./manage.py {" ".join(map(str, args))}')

    def run(self, *args):
        """Execute task."""
        raise NotImplementedError('Task not implemented.')
