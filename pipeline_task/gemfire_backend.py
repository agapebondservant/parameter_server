import requests
import logging
import pyarrow
import traceback
from pipeline_task.backend import Backend
from pipeline_task import config


class GemfireBackend(Backend):
    def __init__(self,
                 region,
                 host=config.gemfire_backend_address):
        super(GemfireBackend, self).__init__(host)
        self.region = region

    def get(self, key):
        value = requests.get(url=f"{self.host}/{self.region}/{key}")
        return value

    def put(self, value, key=None):
        status = requests.post(url=f"{self.host}/{self.region}/{key}",
                               data=value,
                               headers={'Content-Type': 'application/octet-stream'})
        return status
