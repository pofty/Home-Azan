import requests
from bs4 import BeautifulSoup



def get_prayer_times() -> list:
    # URL of the website to scrape
    url = "https://www.muslimpro.com/en/find?country_code=GB&country_name=United%20Kingdom&city_name=London&coordinates=51.5072178,-0.1275862"

    # Send a GET request to the website
    response = requests.get(url)

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful

    # Parse the HTML content using Beautiful Soup and the lxml parser
    soup = BeautifulSoup(response.content, "html.parser")
    # Find all <span> elements with class "jam-solat"
    jam_solat_spans = soup.find_all("span", class_="jam-solat")

    # Extract the values of the <span> elements
    values = [span.text for span in jam_solat_spans]

    prayer_times = []
    # Print the values
    for value in values:
        prayer_times.append(value)

    print(prayer_times)
    return prayer_times

def mock_data() -> list:
    prayer_times = ['20:23', '20:05', '20:27', '17:24', '21:23', '22:44']
    print(prayer_times)
    return prayer_times

