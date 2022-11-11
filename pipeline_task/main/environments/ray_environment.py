import ray
from pipeline_task.main.pipeline_task import PipelineTask
from pipeline_task.main.environments.environment import Environment
from pipeline_task.main.config import config


class RayEnvironment(Environment):
    def __init__(self,
                 host=config.ray_parameter_server_address,
                 params={},
                 runnable_class=PipelineTask,
                 runtime_env={'working_dir': "."}):
        super(RayEnvironment, self).__init__(host)
        ray.init(address=host, runtime_env=runtime_env) if host else ray.init() if not ray.is_initialized() else True
        self.params = params
        self.runnable_class = runnable_class
        self.task = self.initialize_task()

    def initialize_task(self):
        return self.runnable_class.remote(params=self.params)

    def run_worker(self, task_file=None, func=None, input_args=None, input_kwargs=None, output_argnames=None):
        task_id_reference = self.task.invoke.remote(task_file, func, input(), input_kwargs, output_argnames)
        return ray.get(task_id_reference)
