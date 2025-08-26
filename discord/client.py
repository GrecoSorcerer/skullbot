from requests import request
from pprint import pformat
# from os import getenv
# from pprint import pprint
from .discord_logging import (
    DISCORD_API_LOG_MSG,
    log_timestamp
)

class DiscordClient:

    def create_thread(self, discord_api_key, discord_thread_channel_id, new_thread):
        resp = request(
            method="POST",
            headers={
                "Authorization": f"Bot {discord_api_key}",
                "Content-Type": "application/json"
            },
            url=f"https://discord.com/api/v10/channels/{discord_thread_channel_id}/threads",
            json=new_thread
        )
        
        resp_json = resp.json()

        # Log Discord API Response.
        print(DISCORD_API_LOG_MSG.format(
            NOW=log_timestamp(),
            label="create_thread",
            resp=pformat(resp_json, indent=4)
        ))
        return resp_json

    def get_active_threads(self, discord_api_key, discord_server_id):
        resp = request(
            method="GET",
            url=f"https://discord.com/api/v10/guilds/{discord_server_id}/threads/active",
            headers={
                "Authorization": f"Bot {discord_api_key}",
                "Content-Type": "application/json"
            }
        )
        # print(resp.status_code)
        # pprint(resp.json())
        if resp.status_code != 200:
            print(DISCORD_API_LOG_MSG.format(
                NOW = log_timestamp(),
                label="get_active_threads",
                resp=f"Failed to get threads. Request failed,\n{resp.json()["message"]}."
            ))
        
        resp_json = resp.json()

        # Log Discord API Response.
        print(DISCORD_API_LOG_MSG.format(
            NOW=log_timestamp(),
            label="get_active_threads",
            resp="Object filtered, showing 'threads'...\n"+pformat(resp_json["threads"], indent=4)
        ))
        return resp_json
    

    def message_thread(self, discord_api_key, thread, message_content):
        resp = request(
            method="POST",
            url=f"https://discord.com/api/v10/channels/{thread["id"]}/messages",
            headers={
                "Authorization": f"Bot {discord_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "content": message_content,
            }
        )
        
        resp_json = resp.json()

        # Log Discord API Response.
        print(DISCORD_API_LOG_MSG.format(
            NOW=log_timestamp(),
            label="message_thread",
            resp=pformat(resp_json, indent=4)
        ))
        return resp_json

# discord_client = DiscordClient()
# resp = discord_client.get_active_threads(
#     discord_api_key=getenv("DISCORDBOT_KEY"),
#     discord_server_id=getenv("DISCORD_ESCARPMENT_SERVER_ID")
# )
# pprint(resp)