from logging import DEBUG

ENCODING = 'utf-8'

# link
MAIN_LINK = 'https://geekbrains.ru/'
COURSES_LINK_PREFIX = 'education/'
WEBINAR_TYPE_PREFIX = 'lessons/'
VIDEO_TYPE_PREFIX = 'chapters/'
INTERACTIVE_TYPE_PREFIX = 'study_groups/'
WEBINAR_HOMEWORK_PREFIX = 'homework/'
INTERACTIVE_HOMEWORK_PREFIX = 'homeworks/'

# database
DATABASE_PATH = 'sqlite:///storage_gb.db3'

# log
LOGGING_LEVEL = DEBUG
LOGGING_FORMAT = '%(asctime)s - %(levelname)-8s - %(module)s - %(message)s'
LOG_FILE_NAME = 'logs.log'
