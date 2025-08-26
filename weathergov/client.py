from requests import request
from pprint import pprint, pformat
from .weathergov_logging import (
    WEATHERGOV_API_RESPONSE,
    log_timestamp
)

class WeatherGovClient:


    def get_points(self, lat, lon):
        resp = request(
            method="GET",
            url=f"https://api.weather.gov/points/{lat},{lon}",
            headers={
                "Accept":"application/geo json"
            }
        )
        
        resp_json = resp.json()

        # Log Discord API Response.
        print(WEATHERGOV_API_RESPONSE.format(
            NOW=log_timestamp(),
            resp=pformat(resp_json)
        ))
        return resp_json
    
    def get_forecast(self, gridId, gridX, gridY):
        resp = request(
            method="GET",
            url=f"https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast",
            headers={
                "Accept":"application/json"
            }
        )
        
        resp_json = resp.json()

        # Log Discord API Response.
        print(WEATHERGOV_API_RESPONSE.format(
            NOW=log_timestamp(),
            resp=pformat(resp_json)
        ))
        return resp_json

# wg_Client = WeatherGovClient()
# points_data = wg_Client.get_points("42.929459","-78.871376")
# pprint(wg_Client.get_forecast(points_data["properties"]["gridId"], points_data["properties"]["gridX"], points_data["properties"]["gridY"]))
