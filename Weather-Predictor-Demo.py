import requests
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

def get_weather(api_key, location, days=1):
    api_url = f"https://weatherapi-com.p.rapidapi.com/forecast.json?q={location}&days={days}"
    headers = {
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        "X-RapidAPI-Key": api_key,
    }

    response = requests.get(api_url, headers=headers)
    data = response.json()

    if response.status_code == 200 and 'current' in data:
        return data
    elif 'error' in data:
        return {"error": data['error']['message']}
    else:
        return {"error": "Unknown error occurred."}

def reset_ui():
    error_label.config(text="")
    result_label.config(text="")
    for label in forecast_labels:
        label.config(text="")

def search():
    location = location_textfield.get()
    
    if not location:
        error_label.config(text="The location field is empty")
        return

    days = 1 if weather_type_var.get() == "Current" else 5

    reset_ui()

    loading_label.grid(row=2, column=0, columnspan=3, pady=5, sticky='ew')

    window.update_idletasks()

    weather_data = get_weather(api_key, location, days)

    loading_label.grid_forget()

    if 'error' in weather_data:
        error_label.config(text=f"Error: {weather_data['error']}")
    else:
        result_label.config(text="Weather data retrieved successfully.")
        display_weather(weather_data, days)

def display_weather(data, days):
    if days == 1:
        current = data['current']
        temperature = current['temp_c']
        humidity = current['humidity']
        wind_speed = current['wind_kph']
        pressure = current['pressure_mb']
        precipitation = current.get('precip_mm', 0)

        # Update labels with current weather data
        animate_label(temperature_result, f"Temperature: {temperature}°C")
        animate_label(humidity_result, f"Humidity: {humidity}%")
        animate_label(wind_speed_result, f"Wind Speed: {wind_speed} km/h")
        animate_label(pressure_result, f"Pressure: {pressure} hPa")
        animate_label(precipitation_result, f"Precipitation: {precipitation} mm")

        # Hide forecast labels
        for label in forecast_labels:
            label.grid_forget()

    else:
        forecast = data['forecast']['forecastday']
        
        # Update labels with 5-day forecast data if available
        for i, label in enumerate(forecast_labels):
            if i < len(forecast):
                date = forecast[i]['date']
                condition = forecast[i]['day']['condition']['text']
                max_temp = forecast[i]['day']['maxtemp_c']
                min_temp = forecast[i]['day']['mintemp_c']

                label.config(text=f"{date}\nCondition: {condition}\nMax Temp: {max_temp}°C\nMin Temp: {min_temp}°C")
                label.grid(row=9, column=i, padx=10, pady=5, sticky='nsew')
            else:
                label.grid_forget()

        # Hide current weather labels
        animate_label(temperature_result, "")
        animate_label(humidity_result, "")
        animate_label(wind_speed_result, "")
        animate_label(pressure_result, "")
        animate_label(precipitation_result, "")

def animate_label(label, new_text):
    current_text = label.cget("text")
    label.config(text=new_text)

    if current_text != new_text:
        label.update_idletasks()
        label.after(500, lambda: animate_opacity(label, 1.0))

def animate_opacity(label, opacity):
    if opacity > 0:
        label.configure(style="Animated.TLabel")
        label.configure(style="")
        label.after(50, lambda: animate_opacity(label, opacity - 0.1))
    else:
        label.configure(style="TLabel")

# GUI setup
def create_gui():
    global window, api_key, style, frame, location_textfield, error_label, result_label, loading_label
    global weather_type_var, weather_type_radiobuttons, forecast_labels, temperature_result, humidity_result
    global wind_speed_result, pressure_result, precipitation_result

    window = ThemedTk(theme="clam")
    window.title("Weather App")
    window.geometry("800x400")

    api_key = "2cc349ca80msh51baff48f4fc4f1p1dca52jsn627ca1bfe60b"  # Replace with your API key

    style = ttk.Style()
    style.configure('TFrame', background='#EFEFEF', highlightthickness=0)  # Set background color and remove border
    style.configure('TLabel', background='#EFEFEF', font=('Arial', 12))
    style.configure('TButton', font=('Arial', 12))  # Use default button colors
    style.configure('TEntry', font=('Arial', 12), borderwidth=0, highlightbackground='#EFEFEF')  # Remove border


    # Create a Frame widget
    frame = ttk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")

    frame = ttk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    location_label = ttk.Label(frame, text="Location:")
    location_textfield = ttk.Entry(frame, font=('Arial', 12))
    search_button = ttk.Button(frame, text="Search", command=search, style='TButton')
    error_label = ttk.Label(frame, text="", foreground='red', font=('Arial', 10, 'italic'))
    result_label = ttk.Label(frame, text="", foreground='green', font=('Arial', 10, 'italic'))
    loading_label = ttk.Label(frame, text="Loading...", font=('Arial', 10, 'italic'))

    weather_type_var = tk.StringVar(value="Current")
    weather_type_radiobuttons = [
        ttk.Radiobutton(frame, text="Current", variable=weather_type_var, value="Current"),
        ttk.Radiobutton(frame, text="3-Day Forecast", variable=weather_type_var, value="3-Day Forecast")
    ]

    forecast_labels = [ttk.Label(frame, text="", font=('Arial', 12)) for _ in range(5)]

    # Labels
    temperature_label = ttk.Label(frame, text="Temperature:")
    humidity_label = ttk.Label(frame, text="Humidity:")
    wind_speed_label = ttk.Label(frame, text="Wind Speed:")
    pressure_label = ttk.Label(frame, text="Pressure:")
    precipitation_label = ttk.Label(frame, text="Precipitation:")

    # Results
    temperature_result = ttk.Label(frame, text="", font=('Arial', 12, 'bold'))
    humidity_result = ttk.Label(frame, text="", font=('Arial', 12, 'bold'))
    wind_speed_result = ttk.Label(frame, text="", font=('Arial', 12, 'bold'))
    pressure_result = ttk.Label(frame, text="", font=('Arial', 12, 'bold'))
    precipitation_result = ttk.Label(frame, text="", font=('Arial', 12, 'bold'))

    # Grid layout
    location_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
    location_textfield.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
    search_button.grid(row=0, column=2, padx=10, pady=5, sticky='w')
    error_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='ew')
    result_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='ew')
    weather_type_radiobuttons[0].grid(row=3, column=0, padx=10, pady=5, sticky='w')
    weather_type_radiobuttons[1].grid(row=3, column=1, padx=10, pady=5, sticky='w')

    temperature_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
    temperature_result.grid(row=4, column=1, padx=10, pady=5, sticky='w')
    humidity_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
    humidity_result.grid(row=5, column=1, padx=10, pady=5, sticky='w')
    wind_speed_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)
    wind_speed_result.grid(row=6, column=1, padx=10, pady=5, sticky='w')
    pressure_label.grid(row=7, column=0, sticky="w", padx=10, pady=5)
    pressure_result.grid(row=7, column=1, padx=10, pady=5, sticky='w')
    precipitation_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)
    precipitation_result.grid(row=8, column=1, padx=10, pady=5, sticky='w')

    for i, label in enumerate(forecast_labels):
        label.grid(row=9, column=i, padx=10, pady=5, sticky='nsew')

    frame.grid_rowconfigure(10, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    for i in range(5):
        frame.grid_columnconfigure(i, weight=1)

    window.mainloop()

# Run the GUI
create_gui()
