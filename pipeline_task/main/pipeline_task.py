import inspect
import ray
from pipeline_task.main.mappers import task_mapper


@ray.remote
class PipelineTask:
    def __init__(self, params=None):
        self.parameters = params or {}

    def invoke(self, mapping_file=None, func=None, input_args=None, input_kwargs=None, output_argnames=None):
        self.map_attributes(mapping_file, func, input_args, input_kwargs, output_argnames)

        sig = inspect.signature(self.func)
        self.parameters = {**self.parameters, **sig.bind(*self.input_args, **self.input_kwargs).arguments}

        return_value = self.func(*self.input_args, **self.input_kwargs)
        return_value = (return_value,) if type(return_value) is not tuple else return_value
        outputs = (self.output_argnames,) if type(self.output_argnames) is not tuple else self.output_argnames

        self.parameters = {**self.parameters, **dict(zip(outputs, return_value))}
        return self.get_parameters()

    def map_attributes(self, mapping_file=None, func=None, input_args=None, input_kwargs=None, output_argnames=None):
        mapping = task_mapper.from_yaml(mapping_file, self.parameters) if mapping_file else None
        self.func = mapping.get('method') if mapping else func
        self.input_args = mapping.get('input_args') if mapping else input_args
        self.input_kwargs = mapping.get('input_kwargs') if mapping else input_kwargs
        self.output_argnames = mapping.get('outputs') if mapping else output_argnames
        print(f"{self.func} {self.input_kwargs} {self.input_args} {self.output_argnames}")

    def get_parameters(self):
        return self.parameters
