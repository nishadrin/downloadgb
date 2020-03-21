from logging import DEBUG

ENCODING = 'utf-8'

# links
MAIN_LINK = 'https://geekbrains.ru'
COURSES_LINK_PREFIX = '/education'
WEBINAR_TYPE_PREFIX = '/lessons'
VIDEO_TYPE_PREFIX = '/chapters'
INTERACTIVE_TYPE_PREFIX = '/study_groups'
WEBINAR_HOMEWORK_PREFIX = '/homework'
INTERACTIVE_HOMEWORK_PREFIX = '/homeworks'
INTERACTIVE_VIDEOS_PREFIX = '/videos'

# type
WEBINAR_TYPE = 'lesson'
VIDEO_TYPE = 'chapter'
INTERACTIVE_TYPE = 'study_group'
# types
WEBINARS_TYPE = 'lessons'
VIDEOS_TYPE = 'chapters'
# gb type on gb
GB_WEBINAR_TYPE = 'basic'
GB_VIDEO_TYPE = 'video'
GB_INTERACTIVE_TYPE = 'interactive'

# database
DATABASE_PATH = 'sqlite:///storage_gb.db3'

# log
LOGGING_LEVEL = DEBUG
LOGGING_FORMAT = '%(asctime)s - %(levelname)-8s - %(module)s - %(message)s'
LOG_FILE_NAME = 'logs.log'

# not completed courses
STATES_NOT_COMPLETED_COURSES = ('begin', 'continue', 'require_courses')
