import os

from home.commons.Utils.path_utils import get_dir_path

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

LOG_PATH = get_dir_path(SITE_ROOT, "logs")
STATIC_PATH = get_dir_path(SITE_ROOT, "assets", "static")
DATAFILE_PATH = get_dir_path(SITE_ROOT, "assets", "static", "data_file")
STATIC_ZIPFILE_PATH = get_dir_path(SITE_ROOT, "assets", "static", "zipfile")
STATIC_DBBACK_PATH = get_dir_path(SITE_ROOT, "assets", "static", "dbback")
TEMP_PATH = get_dir_path(SITE_ROOT, "temp")
TEMPLATE_PATH = get_dir_path(SITE_ROOT, "assets", "template")
TRANSLATIONS_PATH = get_dir_path(SITE_ROOT, "assets", "translations")
SPIDER_LOG_PATH = get_dir_path(SITE_ROOT, "spiders", "logs")
INIT_SETTINGS_FILE = os.path.join(SITE_ROOT, "init.yaml")
