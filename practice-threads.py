from os import getenv
from requests import request
from pprint import pprint
import datetime

from discord.client import DiscordClient

discord_client = DiscordClient()

from discord.discord_logging import (
    EXCEPTION_MSG,
    DISCORD_API_LOG_MSG,
    log_timestamp
)

print("[Create Practice Threads Start]")

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

saturday = tuesday + datetime.timedelta(days=4)
next_monday = tuesday + datetime.timedelta(days=6)

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
# pprint(payloads)
for new_thread_meta in payloads:
    try:
        resp = discord_client.create_thread(
            discord_api_key=getenv('DISCORDBOT_KEY'),
            discord_thread_channel_id=getenv("DISCORD_THREAD_CHANNEL_ID"),
            new_thread=new_thread_meta
        )
        print(DISCORD_API_LOG_MSG.format(
            NOW=log_timestamp(),
            resp=resp.json()
        ))
    except Exception as e:
        print(EXCEPTION_MSG.format(
            NOW=NOW,
            e=e
        ))


print("[Create Practice Threads End]")