from os import getenv
from pprint import pprint
from datetime import datetime, timedelta

from weathergov.client import WeatherGovClient
from discord.client import DiscordClient

# CONSTANTS (hint: check init files)
from discord import (
    THREAD_NOTIFICATION_MSG_TEMPLATE
)
from discord.discord_logging import (
    EXCEPTION_MSG,
    PARSE_THREADS_LOG_MSG,
    DISCORD_API_LOG_MSG,
    LOG_MSG,
    log_timestamp,
    label_past_present_or_future
)

# Get our Discord API Client
discord_client = DiscordClient()

# Get the current day
TODAY = datetime.today()
# Get today as a string
NOW = f"{TODAY.strftime('%d/%m/%Y - %H:%M:%S')}"

# Start logging for debug purposes
print("[Notify Practice Threads Start]")
print(LOG_MSG.format(
    NOW = log_timestamp(),
    LOG_MSG_BODY="Getting Active Threads..."
))

try:

    # Try to get active threads in our discord server
    resp_json = discord_client.get_active_threads(
        discord_server_id = getenv("DISCORD_ESCARPMENT_SERVER_ID"),
        discord_api_key = getenv("DISCORDBOT_KEY")
    )
except Exception as e:
    print(EXCEPTION_MSG.format(
        NOW=NOW,
        e=e.with_traceback.__str__()
    ))

# Assume that today is Thursday
thursday = TODAY

# Verify that today is Thursday
if thursday.strftime("%A") != "Thursday":
    # Get the difference between today and the scheduled thread
    # creation day, getting the actual day for Thursday if not today.
    thursday = TODAY + timedelta(days=3-TODAY.weekday()) 

# Get Saturday, offset from this Thursday
saturday = thursday + timedelta(days=2)
# Get Next Monday, offset from this Thursday
next_monday = thursday + timedelta(days=6)

# Get the active threads from the json response
pprint(resp_json)
threads = resp_json["threads"]

print(LOG_MSG.format(
    NOW = log_timestamp(),
    LOG_MSG_BODY ="Checking this weeks threads..."
))

# For each active thread in the list of active threads... 
for thread in threads:
    # Get the create_timestamp from the current thread
    thread_create_timestamp = thread["thread_metadata"]["create_timestamp"]
    # Convert the string timestamp to a datetime timestamp
    timestamp = datetime.strptime(
        thread_create_timestamp,
        "%Y-%m-%dT%H:%M:%S.%f%z"
    ).replace(tzinfo=None)

    # If the active thread is from within the last week
    if ((TODAY-timestamp).days.as_integer_ratio()[0] <= 7
        and thread["parent_id"] == getenv("DISCORD_THREAD_CHANNEL_ID")):

        # Get the thread name 
        # Expected: "Practice name MM/DD/YYYY" or "Practice Name MM/DD/YY"
        name:str = thread["name"]
        try:
            # split the thread name and take what we expect to be the date
            # Given "Practice name MM/DD/YYYY" ->  "MM/DD/YYYY"
            practice_date = name.split(" ")[-1]
            # split again for what we'd expect to be mm dd and yyyy, as a list of str
            # Given "MM/DD/YYYY" -> ["MM","DD","YYYY"]
            practice_date_parts = practice_date.split("/")


            # Check year part of practice_date_parts and covert it 
            # to an int to construct datetime `practice_date_as_timestamp`
            if len(practice_date_parts[2]) == 4:
                year = int(practice_date_parts[2])
            elif len(practice_date_parts[2]) == 2:
                year = int(f"{datetime.strftime(TODAY,'%C')}{practice_date_parts[2]}")
            else:
                raise ValueError(f"Bad year format {practice_date_parts[2]}")
            # Get month as an int to construct `practice_date_as_timestamp`
            month = int(practice_date_parts[0])
            # Get day as an int to construct `practice_date_as_timestamp`
            day = int(practice_date_parts[1])

            # try to get the date from `year` `month` and `day` constructed above.
            practice_date_as_timestamp = datetime(year,month,day,tzinfo=None)

            # Log parse event for thread within filter
            print(PARSE_THREADS_LOG_MSG.format(
                NOW = NOW, 
                practice_timestamp_as_date = practice_date_as_timestamp.date(), 
                name = name,
                past_present_future = label_past_present_or_future(TODAY, practice_date_as_timestamp)
            ))
            # pprint(resp.json())
        except Exception as e:
            print(EXCEPTION_MSG.format(
                NOW = NOW,
                e = e.__str__()
            ))
            continue

        # If there is a Practice Thread for today
        if practice_date_as_timestamp.date() == TODAY.date():
            try:
                # Get an instance of our Weather.Gov API Client
                wg_Client = WeatherGovClient()

                # Get the forecast from Weahter.Gov
                forecasts = wg_Client.get_forecast(
                    gridId = getenv("WEATHERGOV_GRIDID"),
                    gridX = getenv("WEATHERGOV_GRIDX"),
                    gridY = getenv("WEATHERGOV_GRIDY")
                )
                # pprint(forecasts)
                # Format Threads Notification Message Content
                content = THREAD_NOTIFICATION_MSG_TEMPLATE.format(
                    forecast_now_name=forecasts["properties"]["periods"][0]["name"],
                    forecast_now=forecasts["properties"]["periods"][0]["detailedForecast"],
                    forecast_later_name=forecasts["properties"]["periods"][1]["name"],
                    forecast_later=forecasts["properties"]["periods"][1]["detailedForecast"]
                )

                # Send notification message to today's thread.
                resp_json = discord_client.message_thread(
                    discord_api_key = getenv("DISCORDBOT_KEY"),
                    thread = thread,
                    message_content = content
                )

                # Log Discord API Response.
                print(DISCORD_API_LOG_MSG.format(
                    NOW=NOW,
                    resp=resp_json
                ))
            except Exception as e:
                print(EXCEPTION_MSG.format(
                    NOW=NOW,
                    e=e.__str__()
                ))
                continue

# End debug logging
print("[Notify Practice Threads END]") 
