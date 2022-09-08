import requests
import logging
import pyarrow
import ray
import traceback
from pipeline_task.backend import Backend
from pipeline_task import config
import gc


class RayBackend(Backend):
    def __init__(self,
                 host=config.ray_backend_address):
        super(RayBackend, self).__init__(host)
        ray.init(address=host)

    def get(self, key: ray.ObjectRef):
        return ray.get(key)

    def put(self, value):
        return ray.put(value)

    def run_worker(self, task_ref: ray.ObjectRef):
        return ray.get(task_ref)

    def finalize(self):
        ray.shutdown()
        gc.collect()

