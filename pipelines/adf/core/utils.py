from itertools import tee

from azureml.pipeline.core import PublishedPipeline

def get_aml_pipe_id(ws, pipe_name): # pylint: disable=unused-variable
  # Loop pipelines
  for p in PublishedPipeline.list(ws):
    if p.name == pipe_name: # return first one with matching name
      return p.id
  return None

def create_or_replace_trigger(adf_client, ws, adf_name, trigger, trigger_name): # pylint: disable=unused-variable
  triggers, _ = tee(adf_client.triggers.list_by_factory(ws.resource_group, adf_name))
  for _, t in enumerate(triggers):
    if t.name == trigger_name:
      return
  adf_client.triggers.create_or_update(ws.resource_group, adf_name, trigger_name, trigger)
  adf_client.triggers.begin_start(ws.resource_group, adf_name, trigger_name)
