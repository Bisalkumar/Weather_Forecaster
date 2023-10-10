import requests
import tkinter as tk
from tkinter import ttk

def get_weather(city_name, units="C"):
    """Fetch the weather data for a given city and forecast for the available days.

    Args:
    - city_name (str): Name of the city.
    - units (str): Desired units for temperature. Either "C" for Celsius or "F" for Fahrenheit.

    Returns:
    - str: Weather information for the city and forecast details.
    """
    # Limit the length of the city name
    if len(city_name) > 100:
        return "City name is too long."
    
    url = f'https://wttr.in/{city_name}?format=j1'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Current Condition
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        if units == "C":
            temperature = current_condition['temp_C']
        else:
            temperature = current_condition['temp_F']

        # Forecast for available days
        forecast = data['weather']
        forecast_str = f"\n\nForecast for the next {len(forecast)} days:\n"
        storm_alerts = []

        for day in forecast:
            date = day['date']
            avg_temp = day['avgtempC'] if units == "C" else day['avgtempF']
            prob_of_rain = day['hourly'][4]['chanceofrain']

            forecast_str += f"{date}: Average Temp: {avg_temp}°{units}, Chance of Rain: {prob_of_rain}%\n"

            # Check for high storm alert (arbitrary condition: wind speed > 50kmph or very high chance of rain)
            if int(day['hourly'][4]['windspeedKmph']) > 50 or int(prob_of_rain) > 80:
                storm_alerts.append(date)

        # Combining all data
        result = f"Weather in {city_name}: {weather_desc}, Temperature: {temperature}°{units}"
        result += forecast_str
        if storm_alerts:
            result += f"\n\nStorm Alert! High storm potential on: {', '.join(storm_alerts)}"

        return result

    except requests.RequestException as e:
        return f"Error Occurred while fetching the weather. Details: {e}"

def fetch_and_display():
    city_name = city_entry.get()
    units_choice = unit_var.get()
    weather_info = get_weather(city_name, units_choice)
    result_text.set(weather_info)

# Create the main window
app = tk.Tk()
app.title("Weather Forecaster")

# Add widgets
frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Enter the name of the City:").grid(column=0, row=0, sticky=tk.W, pady=5)
city_entry = ttk.Entry(frame, width=25)
city_entry.grid(column=1, row=0, sticky=tk.W, pady=5)

unit_var = tk.StringVar()
unit_var.set("C")
ttk.Label(frame, text="Temperature in:").grid(column=0, row=1, sticky=tk.W, pady=5)
ttk.Radiobutton(frame, text="Celsius", variable=unit_var, value="C").grid(column=1, row=1, sticky=tk.W, pady=5)
ttk.Radiobutton(frame, text="Fahrenheit", variable=unit_var, value="F").grid(column=2, row=1, sticky=tk.W, pady=5)

ttk.Button(frame, text="Fetch Weather", command=fetch_and_display).grid(column=1, row=2, pady=20)

result_text = tk.StringVar()
ttk.Label(frame, textvariable=result_text, wraplength=300).grid(column=0, row=3, columnspan=3, pady=5)

# Run the GUI loop
app.mainloop()
