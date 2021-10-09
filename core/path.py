import os

from commons.Utils.path_utils import get_dir_path

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_PATH = get_dir_path(SITE_ROOT, 'logs')
STATIC_PATH = get_dir_path(SITE_ROOT, 'static')
DATAFILE_PATH = get_dir_path(SITE_ROOT, 'static', 'data_file')
STATIC_ZIPFILE_PATH = get_dir_path(SITE_ROOT, 'static', 'zipfile')
STATIC_DBBACK_PATH = get_dir_path(SITE_ROOT, 'static', 'dbback')
TEMP_PATH = get_dir_path(SITE_ROOT, 'temp')
TEMPLATE_PATH = get_dir_path(SITE_ROOT, 'template')
TRANSLATIONS_PATH = get_dir_path(SITE_ROOT, "translations")
SPIDER_LOG_PATH = get_dir_path(SITE_ROOT, 'model_spider', 'model_spider', 'logs')
INIT_SETTINGS_FILE = os.path.join(SITE_ROOT, "init.yaml")
