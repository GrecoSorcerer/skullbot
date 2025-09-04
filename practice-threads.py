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
        "type": 11,  # 11 is for public threads
        "message":{
            "content": "Be mindful, we meet at the same time and place as Flownight; Parking can be hard to find later in the night.",
            "embeds": [{
                "image": {
                    "url": "https://media.discordapp.net/attachments/1409945513998024704/1412071305150468127/image.png?ex=68b6f562&is=68b5a3e2&hm=80f4636e343c7c4a8c1a993e282af1dc3a31cc2cceaa4811014ace6c9901a218&=&format=webp&quality=lossless"
                }
            }]
        }
    },
]

# For each thread to create (`new_thread_meta`) in `payloads`
for new_thread_meta in payloads:
    # try to send the message first, this will 
    try:
        # Call our Discord client to create the thread.
        if new_thread_meta.get("message", False):
            # Sending messages uses the same call as threads, at some point 
            # I will rename message_thread or create a version for channels only
            resp_json = discord_client.message_thread(
                discord_api_key=getenv('DISCORDBOT_KEY'),
                thread={"id":getenv("DISCORD_THREAD_CHANNEL_ID")},
                message_content=new_thread_meta.get("message")
            )

            # Creating the new thread from the message we just created.
            resp_json = discord_client.create_thread_from_message(
                discord_api_key=getenv('DISCORDBOT_KEY'),
                discord_thread_channel_id=getenv("DISCORD_THREAD_CHANNEL_ID"),
                message_id=resp_json["id"],
                new_thread_name=new_thread_meta["name"]
            )

        else:
            # There was no initial message, so just create a thread.
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