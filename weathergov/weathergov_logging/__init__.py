from core.core_logging import (
    LOG_MSG,
    LOG_MSG_HEAD,
    LOG_MSG_FOOT,
    # import to make this available to weathergov/client.py
    log_timestamp
)

WEATHERGOV_API_RESPONSE = \
    LOG_MSG_HEAD +\
    " Weather.GOV Resp. {resp}" +\
    LOG_MSG_FOOT