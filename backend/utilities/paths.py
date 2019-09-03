import os

# path of the backend, from /backend/utilities back to /backend
BACK_DIR = os.path.join(os.path.dirname(__file__), '..')

# directory for all runnable tasks
# the task directory should not be changed, otherwise the task manager will crash
TASK_DIR = os.path.join(BACK_DIR, 'task')
# directory for all tasks' logs
LOG_DIR = os.path.join(BACK_DIR, 'logs')

# dir for all configs
CONFIGS_DIR = os.path.join(BACK_DIR, 'configs')

# path of the config file for connection to postgresql
DATABASE_CONFIG_PATH = os.path.join(CONFIGS_DIR, 'database.ini')
# path of the config file for twitter api
TWITTER_API_CONFIG_PATH = os.path.join(CONFIGS_DIR, 'twitter.ini')
# path of the config file for logging in task manager
LOG_CONFIG_PATH = os.path.join(CONFIGS_DIR, 'logger-conf.json')

NLTK_MODEL_PATH = os.path.join(BACK_DIR, 'models/nltk_model.pickle')

TEXT_CNN_MODEL_PATH = os.path.join(BACK_DIR, 'models/text_cnn_classifier.ckpt')

IMAGE_CLASSIFIER_VGG_PATH = os.path.join(BACK_DIR, 'models/img_classifier_model.ckpt')

IMAGE_CLASSIFIER_RESNET_PATH = os.path.join(BACK_DIR, 'models/ResNet1.ckpt')

EVENT2MIND_MODEL_PATH = os.path.join(BACK_DIR, 'models/event2mind-2018.10.26.tar.gz')

GRIB2_DATA_DIR = os.path.join(BACK_DIR, 'data', 'grib-data')

SOIL_MOIS_DATA_DIR = os.path.join(BACK_DIR, 'data', 'soil-mois-data')

US_SHAPE_PATH = os.path.join(BACK_DIR, 'data', 'US-continental', 'US_continental.shp')

USGS_DATA_DIR = os.path.join(BACK_DIR, 'data', 'usgs')

WIND_DATA_DIR = os.path.join(BACK_DIR, 'data')

GRIB2JSON_PATH = os.path.join('converter', 'bin', 'grib2json')

TWEET_IMAGES_DIR = os.path.join(BACK_DIR, 'data', 'tweet_images')

MODELS_SAVE_PATH = os.path.join(BACK_DIR, 'models')

BOUNDARY_PATH = os.path.join(BACK_DIR, 'data', 'boundaries')

IMAGE_TRAIN_PATH = os.path.join(BACK_DIR, 'data', 'image_dataset/train')

IMAGE_VAL_PATH = os.path.join(BACK_DIR, 'data', 'image_dataset/val')

PRISM_DATA_PATH = os.path.join(BACK_DIR, 'data', 'prism')
