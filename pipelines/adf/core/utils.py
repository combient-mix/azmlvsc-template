from azureml.pipeline.core import PublishedPipeline

def get_aml_pipe_id(ws, pipe_name): # pylint: disable=unused-variable
  # Loop pipelines
  for p in PublishedPipeline.list(ws):
    if p.name == pipe_name: # return first one with matching name
      return p.id
  return None
