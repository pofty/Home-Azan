import re
from datetime import datetime
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

# def get_prayer_times() -> list:
#     url = "https://app.muslimpro.com/prayer-times?lat=51.5072178&lng=-0.1275862&alt=0&country_code=GB"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     # Find JSON-LD script block with prayer times
#     ld_script = soup.select_one("#prayer-times-jsonld")
#     if not ld_script:
#         raise ValueError("Prayer times JSON not found")
#
#     ld = json.loads(ld_script.string)
#
#     # Extract HH:MM times
#     def hhmm(iso: str) -> str:
#         return dt.datetime.fromisoformat(iso.replace("Z","+00:00")).strftime("%H:%M")
#
#     times = {e["name"]: hhmm(e["startDate"]) for e in ld["itemListElement"]}
#
#     # Ordered list [Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha]
#     prayer_times = [
#         times["Fajr"],
#         times["Sunrise"],
#         times["Zuhr"],      # MuslimPro uses "Zuhr" instead of "Dhuhr"
#         times["Asr"],
#         times["Maghrib"],
#         times["Isha"]
#     ]
#
#     print(prayer_times)
#     return prayer_times


def _convert_time_12_to_24(time_str: str, am_pm: Optional[str] = None) -> str:
    """Convert a time string in 12‑hour format to 24‑hour format.

    Parameters
    ----------
    time_str : str
        A string like ``'5:32'`` representing hours and minutes.
    am_pm : Optional[str]
        Either ``'am'``, ``'pm'``, or ``None``.  When ``None`` the time is
        assumed to already be in 24‑hour format and is returned unchanged
        after zero‑padding the hour.

    Returns
    -------
    str
        A string representing the time in 24‑hour format (e.g. ``'05:32'`` or
        ``'15:54'``).  If the original hour is a single digit and no am/pm is
        supplied, the hour is zero‑padded.
    """
    # Normalise the inputs
    time_str = time_str.strip()
    if am_pm:
        am_pm = am_pm.lower().strip('. ')
    # Split into hours and minutes
    try:
        hour_part, minute_part = time_str.split(":")
    except ValueError:
        raise ValueError(f"Invalid time format: '{time_str}'")

    hour = int(hour_part)
    minute = int(minute_part)

    if am_pm in {"am", "pm"}:
        # Convert using datetime for robustness
        dt = datetime.strptime(f"{hour}:{minute:02d} {am_pm}", "%I:%M %p")
        return dt.strftime("%H:%M")
    else:
        # Already 24‑hour; just zero‑pad the hour if necessary
        return f"{hour:02d}:{minute:02d}"


def get_prayer_times(url: str = "https://app.muslimpro.com/prayer-times?lat=51.5072178&lng=-0.1275862"
                                "&alt=0&country_code=GB") -> List[str]:
    """Retrieve today's prayer times from the Muslim Pro prayer‑times page.

    The function attempts to fetch the given URL with headers that mimic a
    standard browser in order to avoid HTTP 403 responses.  It then parses
    the resulting HTML with BeautifulSoup, extracts the sunrise and prayer
    times, converts them to 24‑hour format and returns them in the order
    Fajr, Sunrise, Dhuhur, Asr, Maghrib and Isha.

    Parameters
    ----------
    url : str
        The full URL to the Muslim Pro prayer‑times page for a specific
        location (must include latitude, longitude and country code query
        parameters).

    Returns
    -------
    List[str]
        A list of six time strings in the order ``[Fajr, Sunrise, Dhuhur,
        Asr, Maghrib, Isha]``.  Times are formatted in 24‑hour style, for
        example ``['05:32', '7:00', '12:55', '15:54', '18:39', '19:57']``.

    Raises
    ------
    RuntimeError
        If the prayer times cannot be found on the page.
    requests.HTTPError
        If the HTTP request fails for reasons other than a 200 response.
    """
    # Use headers to emulate a browser; some sites return 403 to scripts
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
    }
    response = requests.get(url, headers=headers)
    # Raise an exception for non‑200 responses (e.g. 403)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the entire visible text to search with regular expressions
    page_text = soup.get_text(separator=" ")

    # 1. Extract sunrise time (present in the Imsak/Sunrise line)【895631104650696†L124-L129】
    sunrise_match = re.search(
        r"Sunrise\s*(\d{1,2}:\d{2})\s*am",
        page_text,
        re.IGNORECASE,
    )
    sunrise_12h = sunrise_match.group(1) if sunrise_match else None

    # 2. Extract prayer times summary (already in 24‑hour for all except Fajr)【895631104650696†L304-L307】
    summary_match = re.search(
        r"Prayer times[^:]*:\s*Faj[ar]{2}?\s*Prayer\s*Time\s*(\d{1,2}:\d{2})\s*,\s*"
        r"Dhuh?ur\s*Prayer\s*Time\s*(\d{1,2}:\d{2})\s*,\s*"
        r"Asr\s*Prayer\s*Time\s*(\d{1,2}:\d{2})\s*,\s*"
        r"Maghrib\s*Prayer\s*Time\s*(\d{1,2}:\d{2})\s*,\s*"
        r"and\s*Isha\s*Prayer\s*Time\s*(\d{1,2}:\d{2})",
        page_text,
        re.IGNORECASE,
    )
    if not summary_match:
        raise RuntimeError("Could not find prayer times summary on the page")

    fajr_12h, dhuhur_24h, asr_24h, maghrib_24h, isha_24h = summary_match.groups()

    # Convert times to 24‑hour; Fajr and sunrise need am/pm context
    fajr_24h = _convert_time_12_to_24(fajr_12h, "am")
    # Sunrise is always in the morning (am)
    sunrise_24h = _convert_time_12_to_24(sunrise_12h, "am") if sunrise_12h else None

    # The remaining times from the summary are already in 24‑hour format
    # but may need zero‑padding on the hour
    dhuhur_24h = _convert_time_12_to_24(dhuhur_24h)
    asr_24h = _convert_time_12_to_24(asr_24h)
    maghrib_24h = _convert_time_12_to_24(maghrib_24h)
    isha_24h = _convert_time_12_to_24(isha_24h)

    # For sunrise, Muslim Pro uses times like '7:00' without leading zero.  To
    # reflect that style, remove any leading zero from the hour.
    if sunrise_24h and sunrise_24h.startswith("0"):
        sunrise_24h_display = sunrise_24h.lstrip("0")
    else:
        sunrise_24h_display = sunrise_24h

    # Assemble the times list in the requested order
    return [
        fajr_24h,
        sunrise_24h_display or "",
        dhuhur_24h,
        asr_24h,
        maghrib_24h,
        isha_24h,
        ]

def mock_data() -> list:
    prayer_times = ['05:11', '06:41', '12:59', '16:14', '19:06', '20:20']
    print(prayer_times)
    return prayer_times