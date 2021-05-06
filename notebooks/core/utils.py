import shutil
import tempfile
from os.path import basename

import joblib
import pandas as pd
from azureml.core import Experiment, Run, Workspace
from azureml.core.model import Model
from azureml.data.dataset_factory import FileDatasetFactory

def get_ws_and_run(experiment_name): # pylint: disable=unused-variable
  run = Run.get_context()
  try:
    ws = run.experiment.workspace
  except AttributeError:
    ws = Workspace.from_config()
    experiment = Experiment(workspace=ws, name=experiment_name)
    run = experiment.start_logging()
  return ws, run

def register_model(run, model, name, tags=None): # pylint: disable=unused-variable
  # Dump model
  tmpdir = tempfile.mkdtemp()
  model_path = f"{tmpdir}/{name}.joblib"
  joblib.dump(value=model, filename=model_path)

  # Upload
  upload_to = f'outputs/{name}.joblib'
  run.upload_file(name=upload_to, path_or_stream=model_path)
  shutil.rmtree(tmpdir)

  # Register
  reg_model = run.register_model(model_name=name, model_path=upload_to, tags=tags)
  return reg_model

def load_model(ws, name): # pylint: disable=unused-variable
  # Download model
  tmpdir = tempfile.mkdtemp()
  Model(ws, name=name).download(target_dir=tmpdir)

  # Load
  model = joblib.load(f"{tmpdir}/{name}.joblib")

  # Clean and return
  shutil.rmtree(tmpdir)
  return model

def lake_load_csv(datastore, in_path, dtype=None, parse_dates=None): # pylint: disable=unused-variable
  # Mount directory
  file_ds = FileDatasetFactory.from_files([(datastore, in_path)])
  mnt_ctx = file_ds.mount()
  mnt_ctx.start()
  mnt_path = mnt_ctx.mount_point

  # Load data
  pd_df = pd.read_csv(f'{mnt_path}/{basename(in_path)}', dtype=dtype, parse_dates=parse_dates)

  # Stop mount
  mnt_ctx.stop()

  # Return
  return pd_df
