import os

# root path of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# directory for all runnable tasks
# the task directory should not be changed, otherwise the task manager will crash
TASK_DIR = os.path.join(ROOT_DIR, 'backend', 'task')
# directory for all tasks' logs
LOG_DIR = os.path.join(ROOT_DIR, 'backend', 'logs')

# dir for all configs
CONFIGS_DIR = os.path.join(ROOT_DIR, 'configs')

# path of the config file for connection to postgresql
DATABASE_CONFIG_PATH = os.path.join(CONFIGS_DIR, 'database.ini')
# path of the config file for twitter api
TWITTER_API_CONFIG_PATH = os.path.join(CONFIGS_DIR, 'twitter.ini')
# path of the config file for logging in task manager
LOG_CONFIG_PATH = os.path.join(CONFIGS_DIR, 'logger-conf.json')

MODELS_SAVE_PATH = os.path.join(ROOT_DIR, 'backend', 'models')

NLTK_MODEL_PATH = os.path.join(MODELS_SAVE_PATH, 'nltk_model.pickle')

TEXT_CNN_MODEL_PATH = os.path.join(MODELS_SAVE_PATH, 'text_cnn_classifier.ckpt')

GOOGLE_VOCAB_PATH = os.path.join(MODELS_SAVE_PATH, 'GoogleNews-vectors-negative300.bin')

IMAGE_CLASSIFIER_VGG_PATH = os.path.join(MODELS_SAVE_PATH, 'img_classifier_model.ckpt')

IMAGE_CLASSIFIER_RESNET_PATH = os.path.join(MODELS_SAVE_PATH, 'ResNet1.ckpt')

EVENT2MIND_MODEL_PATH = os.path.join(MODELS_SAVE_PATH, 'event2mind-2018.10.26.tar.gz')

DATA_PATH = os.path.join(ROOT_DIR, 'data')

TEST_DATA_PATH = os.path.join(DATA_PATH, 'test')

GRIB2_DATA_DIR = os.path.join(DATA_PATH, 'grib-data')

SOIL_MOIS_DATA_DIR = os.path.join(DATA_PATH, 'soil-mois-data')

US_SHAPE_PATH = os.path.join(DATA_PATH, 'US-continental', 'US_continental.shp')

USGS_DATA_DIR = os.path.join(DATA_PATH, 'usgs')

WIND_DATA_DIR = os.path.join(ROOT_DIR, 'backend', 'data')

GRIB2JSON_PATH = os.path.join('converter', 'bin', 'grib2json')

FIRE_DATA_DIR = os.path.join(ROOT_DIR, 'data', 'fire-data')

TWEET_IMAGES_DIR = os.path.join(DATA_PATH, 'tweet_images')

BOUNDARY_PATH = os.path.join(DATA_PATH, 'boundaries')

IMAGE_TRAIN_PATH = os.path.join(DATA_PATH, 'image_dataset/train')

IMAGE_VAL_PATH = os.path.join(DATA_PATH, 'image_dataset/val')

PRISM_DATA_PATH = os.path.join(DATA_PATH, 'prism')
