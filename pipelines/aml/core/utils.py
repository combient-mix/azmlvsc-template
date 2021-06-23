import os
import subprocess

import jupytext
import nbformat as nbf
from azureml.contrib.notebook import (AzureMLNotebookHandler, NotebookRunConfig, NotebookRunnerStep)
from azureml.core import Environment, ScriptRunConfig
from azureml.pipeline.core import PublishedPipeline

def disable_pipeline(ws, name):
  # Disable active pipelines with by name
  for p in PublishedPipeline.list(ws):
    if p.name == name:
      p.disable()

def publish_or_replace_pipeline(ws, pipeline, name): # pylint: disable=unused-variable
  # Disable active pipelines with the same name
  disable_pipeline(ws, name)

  # Publish pipeline
  version = subprocess.check_output(["git", "describe", "--always"]).strip().decode("utf-8")
  return pipeline.publish(
    name=name,
    description=f'version {version}',
    version=version,
  )

def nb_runner_step( # pylint: disable=unused-variable
  notebook_path,
  ws,
  target,
  inputs=None,
  outputs=None,
  conda_env_name='default',
  conda_env_yml='environment.yaml',
  cell_timeout=1200,
  allow_reuse=True,
  **notebook_params,
):
  # Convert jupytext to ipynb and write to ntbkstg
  ntbk = jupytext.read(notebook_path)
  kernelspec = {"display_name": f"Python [conda env:{conda_env_name}]", "language": "python", "name": conda_env_name}
  ntbk['metadata']['kernelspec'] = kernelspec
  ntbkstg_path = os.path.dirname(notebook_path)
  nb_name = os.path.splitext(os.path.basename(notebook_path))[0]
  nbf.write(ntbk, f'{ntbkstg_path}/{nb_name}.stg.ipynb')

  # Setup script run configuration
  compute_target = ws.compute_targets[target]
  env = Environment.from_conda_specification(conda_env_name, file_path=conda_env_yml)
  src = ScriptRunConfig(source_directory=ntbkstg_path, compute_target=compute_target, environment=env)

  # Setup notebook run configuration
  handler = AzureMLNotebookHandler(timeout=cell_timeout)
  nrc = NotebookRunConfig(source_directory=ntbkstg_path,
                          notebook=f'{nb_name}.stg.ipynb',
                          output_notebook=f'outputs/{nb_name}.ipynb',
                          parameters=notebook_params,
                          handler=handler,
                          run_config=src.run_config)

  # Pipeline step
  step = NotebookRunnerStep(
    name=nb_name,
    notebook_run_config=nrc,
    compute_target=compute_target,
    allow_reuse=allow_reuse,
    inputs=inputs,
    outputs=outputs,
  )
  return step
