from datetime import datetime

LOG_MSG_HEAD = \
    "---\n" \
    "[{NOW}]"

LOG_MSG_FOOT = \
    "\n"

LOG_MSG = \
    LOG_MSG_HEAD +\
    " {LOG_MSG_BODY}" +\
    LOG_MSG_FOOT

EXCEPTION_MSG = \
    LOG_MSG_HEAD +\
    " Exception: {e}"

DISCORD_API_LOG_MSG = \
    LOG_MSG_HEAD +\
    " Discord Resp.: {resp}"

PARSE_THREADS_LOG_MSG = \
    LOG_MSG_HEAD +\
    " Parsing Thread [{name}] Nofity Date -> {practice_timestamp_as_date} {past_present_future}"


def label_past_present_or_future(today, timestamp):
    # Returns the label for tagging threads in logs.
    return "PRESENT" if today.date() == timestamp.date() \
      else "PAST" if today.date()>timestamp.date() \
      else "FUTURE"

def log_timestamp():
    return datetime.today().strftime('%d/%m/%Y - %H:%M:%S')