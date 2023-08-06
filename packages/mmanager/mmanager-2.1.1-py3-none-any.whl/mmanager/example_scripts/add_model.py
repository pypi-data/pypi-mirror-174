from requests.api import options
from mmanager.mmanager import Model
secret_key = '0fc94b1d5b7d916d143c070f29bccc1614977c2d'
url = 'http://localhost:8000'
path = 'assets'

model_data = {
    "project": 71,
    "transformerType": "Classification",
    "training_dataset": "/home/mizal/Projects/mmanager/mmanager/assets/model_assets/train.csv",
    "test_dataset": "/home/mizal/Projects/mmanager/mmanager/assets/model_assets/test.csv",
    "pred_dataset": "/home/mizal/Projects/mmanager/mmanager/assets/model_assets/pred.csv",
    "actual_dataset": "/home/mizal/Projects/mmanager/mmanager/assets/model_assets/truth.csv",
    "model_file_path": "/home/mizal/Projects/mmanager/mmanager/assets/model_assets/model.h5",
    "target_column": "label",
    "note": "API TESTTTTTT",
}

Model(secret_key, url).post_model(model_data)
