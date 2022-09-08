from pipeline_task.pipeline_task import PipelineTask
import ray
import joblib
import logging
from pipeline_task.ray_backend import RayBackend
import pandas as pd
import inspect
import re

logging.getLogger().setLevel(logging.INFO)


def random_data(person, place, thing='james'):
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    return person, place, thing, df


backend = RayBackend()

try:
    inputs, input_kwargs, outputs = \
        [("john", "egypt"), ("mary", "france")], [{}, {"thing": "pen"}], [('person', 'place', 'thing', 'df'),
                                                                          ('person2', 'place', 'thing', 'df')]

    for idx in range(len(inputs)):
        # Simulating : Source task - generating output
        source_task_ref = PipelineTask.remote()
        task_output = backend.run_worker(source_task_ref.invoke.remote(
            random_data,
            input_args=inputs[idx],
            input_kwargs=input_kwargs[idx],
            output_argnames=outputs[idx]))
        source_task_output_ref = backend.put(backend.serialize(task_output))

        # Simulating : Source task - sending output to Sink task buffer
        artifact_handle = open(f"params{idx}.pkl", "wb")
        joblib.dump(source_task_output_ref, artifact_handle)
        artifact_handle.close()

        # Simulating : Sink task - receiving input from Source task buffer
        artifact_handle = open(f"params{idx}.pkl", "rb")
        source_task_output_retrieved_ref = joblib.load(artifact_handle)

        # Simulating : Sink task - deserializing input
        source_task_output = backend.deserialize(backend.get(source_task_output_retrieved_ref))
        logging.info(f"Output from Task {idx + 1}: {source_task_output}")

except Exception as e:
    logging.info('Could not complete execution - error occurred: ', exc_info=True)

finally:
    backend.finalize()
