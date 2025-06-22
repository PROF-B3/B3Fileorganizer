def get_weather(city):
    """Fetches weather data for a given city."""
    import requests

    try:
        response = requests.get(f"http://wttr.in/{city}?0")
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    if response is not None and response.status_code == 200:
        try:
            weather_data = response.text
            return weather_data
        except Exception as e:
            print(f"Error processing weather data: {e}")
            return None