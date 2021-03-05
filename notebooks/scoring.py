# %%
# Import deps
import shutil
import tempfile

import joblib
import numpy as np
import pandas as pd
import sklearn as sk
from azureml.core import Datastore, Workspace
from azureml.data.datapath import DataPath
from azureml.data.dataset_factory import TabularDatasetFactory

# Check versions
print('pandas version {}.'.format(pd.__version__))
print('scikit-learn version {}.'.format(sk.__version__))
print('joblib version {}.'.format(joblib.__version__))
print('numpy version {}.'.format(np.__version__))

# %%
# Arguments
param_fileName = 'c_exa_021_PoT_dailyExportForScoring_v3_gold_historicalLoad_20200101_20200803_exportedOn_20200826_pipeID_4d0e9f02-19dc-4fd4-8204-87d914d09da9' # pylint: disable=line-too-long
pipeID = "2f3bd07b-a50e-4d95-b30b-3533a94d99bd"

# %%
# Parameters
filename = f'{param_fileName}.csv.gz'
deployedModel = 'PoT_gbc_1596623330'
deployedScaler = 'fitted_scaler_1596623232'
param_deploymentDate_str = '20200805'
metadataCols = ['WKReservation', 'WKReservationDate_UTC', 'Res_id', 'edwid_res']

# %%
# Get workspace
ws = Workspace.from_config()

# %%
# Define input schema
dytpe_dict = {
  'WKReservation': np.int64, # cdw reservation id
  'Res_id': np.object, # reservation PNR number
  'edwid_res': np.int64, # reservation PNR number
  'dbdPlusOne': np.double, # log(1 + tribe)
  'Psgr_Count': np.double, # log(1 + dbd)
  'tribe': np.double, # dummy,
  'Seg_Count': np.double, # dummy
  'FLAG_OneWay': np.int64, # dummy
  'DaysAtDestinationPlusOne': np.double, # dummy
  'FLAG_PurchasedAncillary': np.int64, # dummy
  'FLAG_bookingType_Agent': np.int64, # dummy
  'FLAG_bookingType_Internet': np.int64, # dummy
  'FLAG_bookingType_OthAirl': np.int64, # dummy
  'FLAG_bookingType_OwnSales': np.int64, # dummy
  'FLAG_weekOrLonger_return': np.int64, # dummy
  'FLAG_CorporateBooking': np.int64, # dummy
  'FLAG_infantInBooking': np.int64, # dummy
  'FLAG_childrenInBooking': np.int64, # dummy
  'FLAG_TravelMonth_01': np.int64, # dummy
  'FLAG_TravelMonth_02': np.int64, # dummy
  'FLAG_TravelMonth_03': np.int64, # dummy
  'FLAG_TravelMonth_04': np.int64, # dummy
  'FLAG_TravelMonth_05': np.int64, # dummy
  'FLAG_TravelMonth_06': np.int64, # dummy
  'FLAG_TravelMonth_07': np.int64, # dummy
  'FLAG_TravelMonth_08': np.int64, # dummy
  'FLAG_TravelMonth_09': np.int64, # dummy
  'FLAG_TravelMonth_10': np.int64, # dummy
  'FLAG_TravelMonth_11': np.int64, # dummy
  'FLAG_TravelMonth_12': np.int64, # dummy
  'FLAG_TravelOut_01': np.int64, # dummy
  'FLAG_TravelOut_02': np.int64, # dummy
  'FLAG_TravelOut_03': np.int64, # dummy
  'FLAG_TravelOut_04': np.int64, # dummy
  'FLAG_TravelOut_05': np.int64, # dummy
  'FLAG_TravelOut_06': np.int64, # dummy
  'FLAG_TravelOut_07': np.int64, # dummy
  'FLAG_TravelIn_01': np.int64, # dummy
  'FLAG_TravelIn_02': np.int64, # dummy
  'FLAG_TravelIn_03': np.int64, # dummy
  'FLAG_TravelIn_04': np.int64, # dummy
  'FLAG_TravelIn_05': np.int64, # dummy
  'FLAG_TravelIn_06': np.int64, # dummy
  'FLAG_TravelIn_07': np.int64, # dummy
  'FLAG_sameLastname': np.int64, # dummy
  'FLAG_tripArea_AFR': np.int64, # dummy
  'FLAG_tripArea_CAM': np.int64, # dummy
  'FLAG_tripArea_DOM': np.int64, # dummy
  'FLAG_tripArea_EUR': np.int64, # dummy
  'FLAG_tripArea_FAE': np.int64, # dummy
  'FLAG_tripArea_MEA': np.int64, # dummy
  'FLAG_tripArea_NAM': np.int64, # dummy
  'FLAG_tripArea_SAM': np.int64, # dummy
  'FLAG_tripArea_SCA': np.int64, # dummy
  'FLAG_tripArea_SWP': np.int64, # dummy
  'FLAG_SK_longhaul': np.int64, # dummy
  'FLAG_SVC_RNK_Hi_Go': np.int64, # dummy
  'FLAG_SVC_RNK_Hi_Plus': np.int64, # dummy
  'FLAG_SVC_RNK_Hi_Business': np.int64, # dummy
  'FLAG_SVC_RNK_Lo_Go': np.int64, # dummy
  'FLAG_SVC_RNK_Lo_Plus': np.int64, # dummy
  'FLAG_SVC_RNK_Lo_Business': np.int64, # dummy
  'FLAG_maxtierLevelInReservation_basic': np.int64, # dummy
  'FLAG_maxtierLevelInReservation_silver': np.int64, # dummy
  'FLAG_maxtierLevelInReservation_gold': np.int64, # dummy
  'FLAG_maxtierLevelInReservation_diamond': np.int64, # dummy
  'FLAG_maxtierLevelInReservation_pandion': np.int64, # dummy
}

parse_dates = ['WKReservationDate_UTC'] # reservation date

# %%
# Load data
ws = Workspace.from_config()
datastore = Datastore.get(ws, 'saswecomexa_projects')

# Can't read gzipped so need to download first
tmp_path = tempfile.gettempdir() + '/' + next(tempfile._get_candidate_names())
prefix = f'021/in/{filename}'
datastore.download(tmp_path, prefix)

# Load in memory
pd_df = pd.read_csv(f'{tmp_path}/{prefix}', dtype=dytpe_dict, parse_dates=parse_dates)

# Remove tmp
shutil.rmtree(tmp_path)

# %%
# Check that there are no missing values
pd_df_null = pd_df[pd_df.isnull().any(axis=1)]
assert pd_df_null.shape[0] == 0

# %%
# Display for debug
pd_df_null

# %%
# Load model and column scaler

# Setup paths
tmp_path = tempfile.gettempdir() + '/' + next(tempfile._get_candidate_names())
model_path = f'021/models/{deployedModel}.joblib'
scaler_path = f'021/models/{deployedScaler}.joblib'

# Download model and scaler (not registered in AzureML)
prefix = f'021/in/{filename}'
datastore.download(tmp_path, model_path)
datastore.download(tmp_path, scaler_path)

# Load in memory
trainedModel = joblib.load(f'{tmp_path}/{model_path}')
fittedScaler = joblib.load(f'{tmp_path}/{scaler_path}')

# Remove tmp
shutil.rmtree(tmp_path)

# %%
# Divide dataset into features and metadata
# Get all columns from the dataframe except the ones defined above as metadata columns
featuresCols = np.setdiff1d(list(pd_df.columns), metadataCols).tolist()
metadata_reservations = pd_df[metadataCols]
features = pd_df[featuresCols]

# Apply the scaler
num_cols = ['dbdPlusOne', 'Psgr_Count', 'tribe', 'Seg_Count', 'DaysAtDestinationPlusOne']
features[num_cols] = fittedScaler.transform(features[num_cols])

# Predict class probabilities and store them in a pandas dataframe
class_probabilities = pd.DataFrame(trainedModel.predict_proba(features))

# Predict class label and store them in a pandas dataframe
class_label = pd.DataFrame(trainedModel.predict(features))

# Append columns from previous dataframes
res = pd.concat([class_probabilities, class_label], axis=1, sort=False)

# Rename columns
res.columns = ['prob_leisure', 'prob_business', 'label_businessIs1']

# Join predictions with metadatacolumns by index number
print(metadata_reservations.shape[0], res.shape[0]) #check that they have equal lenght
res2 = metadata_reservations.join(res)
print(res2.shape[0])

# %%
# Add metadata about the run
res2['model'] = f'{deployedModel}_deployedOn_{param_deploymentDate_str}'
res2['input_fileName'] = filename
res2['pipe_runID'] = pipeID
res2['prediction_tms_utc'] = pd.Timestamp.utcnow()

# %%
# For debugging
res2.head(2)

# %%
# Store file in lake
filenameWithoutExtension = filename.split('.')[0]
processed_filename_withPath = f'021/out/{filenameWithoutExtension}.parquet'
print(processed_filename_withPath)

# Store in sasweucomexa lake as a parquet file
dataset = TabularDatasetFactory.register_pandas_dataframe(
  res2,
  name=filenameWithoutExtension,
  target=DataPath(datastore, processed_filename_withPath),
)
dataset.register(workspace=ws, name=filenameWithoutExtension)
