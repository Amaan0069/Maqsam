#!/usr/bin/env python3
import sys
import urllib.request
import json
from datetime import datetime, timezone, timedelta

def fetch_sun_times(lat, lon):
    # Build the API URL with formatted time
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
    except Exception as e:
        print("Error fetching sun times:", e)
        sys.exit(1)
    return data['results']

def main():
    # Ensure exactly two arguments latitude and longitude are provided
    if len(sys.argv) != 3:
        print("Usage: ./wallpaper_selector.py <latitude> <longitude>")
        sys.exit(1)
    
    try:
        lat = float(sys.argv[1])
        lon = float(sys.argv[2])
    except ValueError:
        print("Invalid latitude or longitude. Please provide valid numbers.")
        sys.exit(1)
    
    # Fetch sunrise and sunset times from the API
    sun_times = fetch_sun_times(lat, lon)
    
    # Convert the API times from ISO format to datetime objects (in UTC)
    sunrise = datetime.fromisoformat(sun_times['sunrise'])
    sunset = datetime.fromisoformat(sun_times['sunset'])
    
    # Get the current time in UTC
    now = datetime.now(timezone.utc)
    
    # Determine which wallpaper to use based on the time of day
    if now < sunrise or now > sunset:
        print("night.png")
    else:
        sunrise_window_end = sunrise + timedelta(minutes=30)
        if sunrise <= now <= sunrise_window_end:
            print("sunrise.png")
        else:
            print("morning.png")

if __name__ == "__main__":
    main()
