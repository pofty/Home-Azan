import requests
from bs4 import BeautifulSoup
import json
import datetime as dt

def get_prayer_times() -> list:
    url = "https://www.muslimpro.com/en/find?country_code=GB&country_name=United%20Kingdom&city_name=London&coordinates=51.5072178,-0.1275862"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find JSON-LD script block with prayer times
    ld_script = soup.select_one("#prayer-times-jsonld")
    if not ld_script:
        raise ValueError("Prayer times JSON not found")

    ld = json.loads(ld_script.string)

    # Extract HH:MM times
    def hhmm(iso: str) -> str:
        return dt.datetime.fromisoformat(iso.replace("Z","+00:00")).strftime("%H:%M")

    times = {e["name"]: hhmm(e["startDate"]) for e in ld["itemListElement"]}

    # Ordered list [Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha]
    prayer_times = [
        times["Fajr"],
        times["Sunrise"],
        times["Zuhr"],      # MuslimPro uses "Zuhr" instead of "Dhuhr"
        times["Asr"],
        times["Maghrib"],
        times["Isha"]
    ]

    print(prayer_times)
    return prayer_times

def mock_data() -> list:
    prayer_times = ['05:11', '06:41', '12:59', '16:14', '19:06', '20:20']
    print(prayer_times)
    return prayer_times
