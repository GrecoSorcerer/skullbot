from os import getenv
from requests import request
from pprint import pprint
import datetime

print("[Create Practice Threads Start]")

today = datetime.date.today()
# Get the current day
TODAY = today
# Get today as a string
NOW = f"{TODAY.strftime('%d/%m/%Y - %H:%M:%S')}"


LOG_MSG_HEAD = \
    "---\n" \
    "[{NOW}]"
EXCEPTION_MSG = \
    LOG_MSG_HEAD +\
    "Exception: {e}"
DISCORD_API_LOG_MSG = \
    LOG_MSG_HEAD +\
    "Discord Resp.: {resp}"

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
for payload in payloads:
    try:
        response = request(
            method="POST",
            headers={
                "Authorization": f"Bot {getenv('DISCORDBOT_KEY')}",
                "Content-Type": "application/json"
            },
            url=f"https://discord.com/api/v10/channels/{getenv("DISCORD_THREAD_CHANNEL_ID")}/threads",
            json=payload
        )
        print(DISCORD_API_LOG_MSG.format(
            NOW=NOW,
            response=response.json()
        ))
    except Exception as e:
        print(EXCEPTION_MSG.format(
            NOW=NOW,
            e=e
        ))


print("[Create Practice Threads End]")