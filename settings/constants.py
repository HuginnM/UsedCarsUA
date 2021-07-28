import os

WEB_VERSION = True
SECRET_KEY = os.urandom(32)
DATA_FOLDER = 'data'
TRAIN_CSV = os.path.join(DATA_FOLDER, 'train.csv')
VAL_CSV = os.path.join(DATA_FOLDER, 'val.csv')
SAVED_ESTIMATOR = os.path.join('models', 'xgbr.pickle')
