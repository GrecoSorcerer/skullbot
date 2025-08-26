from core.core_logging import (
    LOG_MSG,
    LOG_MSG_PREFIX,
    LOG_MSG_HEAD,
    LOG_MSG_FOOT,
    EXCEPTION_MSG,
    # import to make this available to discord/client.py
    log_timestamp
)

DISCORD_API_LOG_MSG = \
    LOG_MSG_HEAD +\
    LOG_MSG_PREFIX + " Discord Resp.:\n{resp}" +\
    LOG_MSG_FOOT

PARSE_THREADS_LOG_MSG = \
    LOG_MSG_HEAD +\
    " Parsing Thread [{name}] Nofity Date -> {practice_timestamp_as_date} {past_present_future}" +\
    LOG_MSG_FOOT


def label_past_present_or_future(today, timestamp):
    # Returns the label for tagging threads in logs.
    return "PRESENT" if today.date() == timestamp.date() \
      else "PAST" if today.date()>timestamp.date() \
      else "FUTURE"