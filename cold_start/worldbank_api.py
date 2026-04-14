import requests

class WorldBankAPI:

    BASE_URL = "https://api.worldbank.org/v2/country"

    INDICATORS = {
        "gdp": "NY.GDP.PCAP.CD",
        "internet": "IT.NET.USER.ZS",
        "population": "SP.POP.TOTL"
    }

    def __init__(self, country_code):
        self.country_code = country_code

    def fetch_indicator(self, indicator):
        url = f"{self.BASE_URL}/{self.country_code}/indicator/{indicator}?format=json&per_page=10"

        try:
            response = requests.get(url)
            data = response.json()

            if len(data) > 1:
                for entry in data[1]:
                    if entry["value"] is not None:
                        return entry["value"]

            return None

        except:
            return None

    def get_country_data(self):
        return {
            "gdp_per_capita": self.fetch_indicator(self.INDICATORS["gdp"]),
            "internet_penetration": self.fetch_indicator(self.INDICATORS["internet"]),
            "population": self.fetch_indicator(self.INDICATORS["population"])
        }