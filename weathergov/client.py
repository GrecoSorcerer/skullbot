from requests import request
from pprint import pprint


class WeatherGovClient:


    def get_points(self, lat, lon):
        resp = request(
            method="GET",
            url=f"https://api.weather.gov/points/{lat},{lon}",
            headers={
                "Accept":"application/geo json"
            }
        )
        return resp.json()
    
    def get_forecast(self, gridId, gridX, gridY):
        resp = request(
            method="GET",
            url=f"https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast",
            headers={
                "Accept":"application/json"
            }
        )
        return resp.json()

# wg_Client = WeatherGovClient()
# points_data = wg_Client.get_points("42.929459","-78.871376")
# pprint(wg_Client.get_forecast(points_data["properties"]["gridId"], points_data["properties"]["gridX"], points_data["properties"]["gridY"]))
