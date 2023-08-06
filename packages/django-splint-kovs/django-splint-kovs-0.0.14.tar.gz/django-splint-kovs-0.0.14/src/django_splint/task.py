from .utils.aws.ecs import AWSECSHandler


class SplintTask(AWSECSHandler):
    def __init__(self):
        """Constructor."""
        self.module = self.__class__.__module__
        self.clazz = self.__class__.__name__
        super().__init__()

    def delay(self, *args):
        """Run task in AWS ECS."""
        return AWSECSHandler().run_task(
            command=f'python manage.py  {self.command_name} {self.module} {self.clazz} ' + 
            ' '.join(map(lambda x: str(x), args)))

    def run(self, *args):
        """Execute task."""
        raise NotImplementedError('Task not implemented.')
