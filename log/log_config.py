import os
import sys
from logging import getLogger, Formatter, StreamHandler, ERROR, handlers

from common.config import ENCODING, LOGGING_LEVEL, LOGGING_FORMAT, LOG_FILE_NAME

# create path to save logs
try:
    os.mkdir(f'{os.path.join(os.path.dirname(__file__))}/log_files')
    PATH = os.path.join(os.path.dirname(__file__), f'log_files/{LOG_FILE_NAME}')
except OSError:
    PATH = os.path.join(os.path.dirname(__file__), f'log_files/{LOG_FILE_NAME}')

LOG = getLogger('logger_gb')
GB_FORMATTER = Formatter(LOGGING_FORMAT)

# create handler stderr
ERROR_HANDLER = StreamHandler(sys.stderr)
ERROR_HANDLER.setFormatter(GB_FORMATTER)
ERROR_HANDLER.setLevel(ERROR)

LOG_FILE = handlers.TimedRotatingFileHandler(PATH, encoding=ENCODING,
                                             interval=1, when='M')

LOG_FILE.setFormatter(GB_FORMATTER)
LOG.setLevel(LOGGING_LEVEL)

LOG.addHandler(ERROR_HANDLER)
LOG.addHandler(LOG_FILE)
