import inspect
import ray


@ray.remote
class PipelineTask:
    def __init__(self, params=None):
        self.parameters = params or {}
        self.ack = False

    def invoke(self, func, input_args=(), input_kwargs={}, output_argnames=()):
        sig = inspect.signature(func)
        self.parameters = {**self.parameters, **sig.bind(*input_args, **input_kwargs).arguments}

        return_value = func(*input_args, **input_kwargs)
        return_value = (return_value,) if type(return_value) is not tuple else return_value
        outputs = (output_argnames,) if type(output_argnames) is not tuple else output_argnames

        # if len(return_value) != len(outputs):
        #    raise ValueError(f'The number of expected outputs ({len(outputs)})'
        #                     f' does not match the number of values returned by method {func.__name__}() ({len(return_value)})')

        self.parameters = {**self.parameters, **dict(zip(outputs, return_value))}
        return self.get_parameters()

    def get_parameters(self):
        return self.parameters
