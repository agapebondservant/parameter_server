import requests
import logging
import pyarrow
import ray
import traceback
from pipeline_task.main.parameter_server import ParameterServer
from pipeline_task.main import config
import gc


class RayParameterServer(ParameterServer):
    def __init__(self,
                 host=config.ray_parameter_server_address,
                 runtime_env={'working_dir': "."}):
        super(RayParameterServer, self).__init__(host)
        ray.init(address=host, runtime_env=runtime_env) if not ray.is_initialized() else True

    def get(self, key: ray.ObjectRef):
        return self.deserialize(ray.get(key))

    def put(self, value):
        return ray.put(self.serialize(value))

    def finalize(self):
        ray.shutdown()
        gc.collect()

