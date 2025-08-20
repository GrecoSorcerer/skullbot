THREAD_NOTIFICATION_MSG_HEAD = "<@&1216498625899790486>"
THREAD_NOTIFICATION_MSG_BODY_TEMPLATE = \
    "> **{forecast_now_name}**\n" \
    "> {forecast_now}\n" \
    "> \n" \
    "> **{forecast_later_name}**\n" \
    "> {forecast_later}" \
    "\n\n" \
    "If you're planning to attend today's practice, don't forget to give this channel a shout!"
THREAD_NOTIFICATION_MSG_FOOT = ""

THREAD_NOTIFICATION_MSG_TEMPLATE = \
    f"{THREAD_NOTIFICATION_MSG_HEAD}\n\n" \
    f"{THREAD_NOTIFICATION_MSG_BODY_TEMPLATE}\n" \
    f"{THREAD_NOTIFICATION_MSG_FOOT}\n"