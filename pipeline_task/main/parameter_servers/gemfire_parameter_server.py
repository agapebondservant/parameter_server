import requests
from pipeline_task.main.parameter_servers.parameter_server import ParameterServer
from pipeline_task.main.config import config


class GemfireParameterServer(ParameterServer):
    def __init__(self,
                 region,
                 host=config.gemfire_parameter_server_address):
        super(GemfireParameterServer, self).__init__(host)
        self.region = region

    def get(self, key):
        value = requests.get(url=f"{self.host}/{self.region}/{key}")
        return value

    def put(self, value, key=None):
        status = requests.post(url=f"{self.host}/{self.region}/{key}",
                               data=value,
                               headers={'Content-Type': 'application/octet-stream'})
        return status
