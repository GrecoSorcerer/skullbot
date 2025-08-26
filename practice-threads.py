from os import getenv
from requests import request
from pprint import pprint
import datetime

from discord.client import DiscordClient

discord_client = DiscordClient()

from discord.discord_logging import (
    EXCEPTION_MSG,
    LOG_MSG,
    log_timestamp
)

# Report start of logging
print(LOG_MSG.format(
    NOW = log_timestamp(),
    LOG_MSG_BODY="[Create Practice Threads START]"
))

today = datetime.date.today()
# Get the current day
TODAY = today
# Get today as a string
NOW = f"{TODAY.strftime('%d/%m/%Y - %H:%M:%S')}"

tuesday = today # Assume today is tuesday

if today.strftime("%A") != "Tuesday":
    # Get the difference between today and the scheduled thread
    # creation day.
    tuesday = today + datetime.timedelta(days=1-today.weekday()) 

# Get Saturday, offset from this Tuesday
saturday = tuesday + datetime.timedelta(days=4)
# Get Next Monday, offset from this Tuesday
next_monday = tuesday + datetime.timedelta(days=6)

# The practice threads to be created
payloads = [
    {
        "name": f"Saturday Practice {saturday.strftime('%m/%d/%Y')}",
        "auto_archive_duration": 10080,
        "type": 11  # 11 is for public threads
    },
    {
        "name": f"Monday Practice {next_monday.strftime('%m/%d/%Y')}",
        "auto_archive_duration": 10080,
        "type": 11  # 11 is for public threads
    },
]

# For each thread to create (`new_thread_meta`) in `payloads`
for new_thread_meta in payloads:
    try:
        # Call our Discord client to create the thread.
        resp_json = discord_client.create_thread(
            discord_api_key=getenv('DISCORDBOT_KEY'),
            discord_thread_channel_id=getenv("DISCORD_THREAD_CHANNEL_ID"),
            new_thread=new_thread_meta
        )
    except Exception as e:
        # Something happened, log it.
        print(EXCEPTION_MSG.format(
            NOW=log_timestamp(),
            e=e
        ))

# Report end of logging
print(LOG_MSG.format(
    NOW = log_timestamp(),
    LOG_MSG_BODY="[Create Practice Threads END]"
))