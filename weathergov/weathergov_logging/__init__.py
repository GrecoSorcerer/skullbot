from core.core_logging import (
    LOG_MSG,
    LOG_MSG_HEAD,
    LOG_MSG_FOOT,
    # import to make this available to weathergov/client.py
    log_timestamp
)

WEATHERGOV_API_RESPONSE = \
    LOG_MSG_HEAD +\
    " Weather.GOV Resp.\n{resp}" +\
    LOG_MSG_FOOT

WEATHERGOV_LOG_PERIOD_HEADER =\
    " Forecasts..                Name | Detailed Forecast\n"

WEATHERGOV_LOG_PERIOD = \
    "{period_name:>32} | {period_detailed_forecast:<}"
