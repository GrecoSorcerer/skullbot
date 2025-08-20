from requests import request
# from os import getenv
# from pprint import pprint
from .discord_logging import (
    LOG_MSG,
    log_timestamp
)

class DiscordClient:

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
            print(LOG_MSG.format(
                NOW = log_timestamp(),
                LOG_MSG_BODY=f"Failed to get threads. Request failed, {resp.json()["message"]}."
            ))
        return resp.json()
    

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

        return resp.json()

# discord_client = DiscordClient()
# resp = discord_client.get_active_threads(
#     discord_api_key=getenv("DISCORDBOT_KEY"),
#     discord_server_id=getenv("DISCORD_ESCARPMENT_SERVER_ID")
# )
# pprint(resp)