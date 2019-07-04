import os

# root path of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# path of the config file for connection to postgresql
DATABASE_CONFIG_PATH = os.path.join(ROOT_DIR, 'configs/database.ini')

NLTK_MODEL_PATH = os.path.join(ROOT_DIR, 'backend/models/nltk_model.pickle')
