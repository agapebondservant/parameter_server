from pipeline_task.main.pipeline_task import PipelineTask
import joblib
import logging
from pipeline_task.main.ray_environment import RayEnvironment
from pipeline_task.main.ray_parameter_server import RayParameterServer
import os
from os import listdir

logging.getLogger().setLevel(logging.INFO)

environment = RayEnvironment(params={'person': 'john', 'place': 'egypt', 'person2': 'mary'},
                             runnable_class=PipelineTask)
parameter_server = RayParameterServer()
yaml_dir = 'pipeline_task/tests/data'

try:
    for idx, file in enumerate(listdir(yaml_dir)):
        # Simulating : Source task - generating output
        output = environment.run_worker(os.path.join(yaml_dir, file))
        output_reference = parameter_server.put(output)

        # Simulating : Source task - sending output to Sink task buffer
        artifact_handle = open(f"params{idx}.pkl", "wb")
        joblib.dump(output_reference, artifact_handle)
        artifact_handle.close()

        # Simulating : Sink task - receiving input from Source task buffer
        artifact_handle = open(f"params{idx}.pkl", "rb")
        retrieved_output_reference = joblib.load(artifact_handle)

        # Simulating : Sink task - deserializing input
        source_task_output = parameter_server.get(retrieved_output_reference)
        logging.info(f"Output from Task {idx + 1}: {source_task_output}")

except Exception as e:
    logging.info('Could not complete execution - error occurred: ', exc_info=True)

finally:
    parameter_server.finalize()
