from tkinter import *
import customtkinter
import requests

# setting theme
customtkinter.set_appearance_mode("dark")

# create component
# customtkinter.set_default_color_theme("green")

# create CTK
root = customtkinter.CTk()

# setting width height
root.geometry("400x600")  # Adjusted the window size

# Label for instructions
instruction_label = customtkinter.CTkLabel(
    master=root, text="Enter a location name:")
instruction_label.place(relx=0.5, rely=0.2, anchor=CENTER)

# Entry widget for location input
location_entry = customtkinter.CTkEntry(master=root)
location_entry.place(relx=0.5, rely=0.25, anchor=CENTER)

# Button to get weather

def get_weather_callback():
    location_name = location_entry.get()
    get_weather(location_name)

# Function to simulate clicking the "Get Weather" button


def trigger_get_weather(event):
    get_weather_button.invoke()


# Bind the <Return> key to trigger the button
location_entry.bind("<Return>", trigger_get_weather)

# Button to get weather
get_weather_button = customtkinter.CTkButton(
    master=root, text="Get Weather", command=get_weather_callback, bg_color="#000000")
get_weather_button.place(relx=0.5, rely=0.324, anchor=CENTER)
# Create a CTkTextbox widget for displaying weather information
weather_text = customtkinter.CTkTextbox(master=root, state="disabled")
weather_text.place(relx=0.5, rely=0.6, anchor=CENTER)

# Configure textbox to be read-only and set text color, background color, and font
weather_text.configure(
    state="disabled",
    fg_color=("#FFFFFF", "#3A3B3C"),  # Text color (light and dark)
    bg_color="#2A2B2C",  # Background color for dark theme
    font=("Poppins", 16),  # Font family and size
    wrap="word",  # Wrap text by words
    padx=10,  # Horizontal padding
    pady=5,  # Vertical padding
    border_width=0  # Remove the border around the textbox
)

# Function to display weather information in the text widget


def display_weather_info(info):
    weather_text.configure(state="normal")
    weather_text.delete("0.0", "end")
    weather_text.insert("0.0", info)
    weather_text.configure(state="disabled")


def get_coordinates(location_name):
    try:
        # Construct the URL for the Nominatim Geocoding API
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location_name,
            "format": "json",
        }

        # Send a GET request to the Nominatim API
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Extract the coordinates from the response
        if data and len(data) > 0:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        else:
            raise Exception("Geocoding failed. Location not found.")

    except requests.exceptions.HTTPError as http_err:
        display_weather_info(f"HTTP error occurred: {http_err}")
    except Exception as err:
        display_weather_info(f"An error occurred during geocoding: {err}")
    return None, None


def get_weather(location_name):
    latitude, longitude = get_coordinates(location_name)

    if latitude is not None and longitude is not None:
        try:
            # Construct the API URL with custom latitude and longitude
            location_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,rain,windspeed_10m&current_weather=true"

            # Send a GET request to the Open-Meteo API
            response = requests.get(location_url)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()

            # Create a string to display weather information
            weather_info = f"Weather in {location_name}:\n"
            current_weather = data.get('current_weather', {})
            for key, value in current_weather.items():
                weather_info += f"{key.capitalize()}: {value}\n"

            # Display weather information in the CTkTextbox
            display_weather_info(weather_info)

        except requests.exceptions.HTTPError as http_err:
            display_weather_info(f"HTTP error occurred: {http_err}")
        except Exception as err:
            display_weather_info(f"An error occurred: {err}")
    else:
        display_weather_info(
            f"Failed to obtain coordinates for {location_name}")


if __name__ == "__main__":
    root.mainloop()
