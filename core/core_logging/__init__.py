from datetime import datetime

LOG_MSG_HEAD = \
    ""
LOG_MSG_PREFIX = \
    "[{NOW}]"

LOG_MSG_FOOT = \
    "\n"

LOG_MSG = \
    LOG_MSG_HEAD +\
    LOG_MSG_PREFIX + " {LOG_MSG_BODY}" +\
    LOG_MSG_FOOT

EXCEPTION_MSG = \
    LOG_MSG_HEAD +\
    " Exception: {e}" +\
    LOG_MSG_FOOT


def log_timestamp():
    return datetime.today().strftime('%d/%m/%Y - %H:%M:%S')