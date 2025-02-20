import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import pygame
import random
import math

# Initialize pygame for sound effects
pygame.mixer.init()

# Weather API configuration
API_KEY = "b3d9eb3d02a80dd7660c000017d9eac1"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"

# Weather effects classes
class WeatherEffect:
    def __init__(self, canvas):
        self.canvas = canvas
        self.objects = []
        
    def update(self):
        pass

class RainEffect(WeatherEffect):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.create_rain()
        pygame.mixer.music.load("rain.mp3")
        pygame.mixer.music.play(-1)
        
    def create_rain(self):
        for _ in range(150):
            x = random.randint(0, 800)
            y = random.randint(-500, 0)
            length = random.randint(5, 15)
            self.objects.append(self.canvas.create_line(
                x, y, x, y + length, fill="#6495ED", width=2))
                
    def update(self):
        for drop in self.objects:
            self.canvas.move(drop, 0, 5)
            pos = self.canvas.coords(drop)
            if pos[1] > 600:
                self.canvas.move(drop, 0, -650)

class SnowEffect(WeatherEffect):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.create_snow()
        pygame.mixer.music.load("s snow.mp3")
        pygame.mixer.music.play(-1)
        
    def create_snow(self):
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(-500, 0)
            size = random.randint(2, 5)
            self.objects.append(self.canvas.create_oval(
                x, y, x + size, y + size, fill="white", outline=""))
                
    def update(self):
        for flake in self.objects:
            self.canvas.move(flake, random.randint(-1, 1), 3)
            pos = self.canvas.coords(flake)
            if pos[1] > 600:
                self.canvas.move(flake, 0, -650)

class SunEffect(WeatherEffect):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.create_sun()
        
    def create_sun(self):
        # Create sun rays
        for angle in range(0, 360, 30):
            x1 = 700 + 50 * math.cos(math.radians(angle))
            y1 = 50 + 50 * math.sin(math.radians(angle))
            self.objects.append(self.canvas.create_line(
                700, 50, x1, y1, fill="yellow", width=3))
        # Create sun circle
        self.objects.append(self.canvas.create_oval(
            675, 25, 725, 75, fill="yellow", outline=""))
                
    def update(self):
        # Rotate sun rays
        for ray in self.objects[:-1]:
            self.canvas.move(ray, 0.5, 0)
            if self.canvas.coords(ray)[0] > 800:
                self.canvas.move(ray, -800, 0)

class CloudEffect(WeatherEffect):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.create_clouds()
        
    def create_clouds(self):
        # Create multiple clouds
        for i in range(3):
            x = random.randint(0, 800)
            y = random.randint(50, 150)
            self.objects.append(self.canvas.create_oval(
                x, y, x + 150, y + 50, fill="white", outline="gray"))
                
    def update(self):
        for cloud in self.objects:
            self.canvas.move(cloud, 1, 0)
            pos = self.canvas.coords(cloud)
            if pos[0] > 800:
                self.canvas.move(cloud, -900, 0)

class HazeEffect(WeatherEffect):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.create_haze()
        
    def create_haze(self):
        for _ in range(50):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.randint(10, 30)
            self.objects.append(self.canvas.create_oval(
                x, y, x + size, y + size, fill="gray", outline="", stipple="gray50"))
                
    def update(self):
        for particle in self.objects:
            self.canvas.move(particle, random.randint(-1, 1), random.randint(-1, 1))

# Main application class
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x600")
        
        # Load background image
        self.bg_image = ImageTk.PhotoImage(Image.open("weather.jpg"))
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.canvas.pack()
        
        # Add UI elements
        self.create_widgets()
        
        # Initialize weather effect
        self.current_effect = None
        
    def create_widgets(self):
        # City entry
        self.city_entry = tk.Entry(self.root, font=("Arial", 16))
        self.city_entry.place(x=50, y=50, width=200, height=30)
        
        # Search button
        self.search_btn = tk.Button(self.root, text="Get Forecast", 
                                   command=self.get_weather)
        self.search_btn.place(x=260, y=50, width=120, height=30)
        
        # Weather display
        self.weather_label = tk.Label(self.root, font=("Arial", 16), 
                                     bg="white", justify="left", anchor="nw")
        self.weather_label.place(x=50, y=100, width=700, height=450)

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
            
        complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric&lang=en"
        try:
            response = requests.get(complete_url)
            print(f"API Response: {response.text}")  # Debug print
            data = response.json()
            print(f"Parsed Data: {data}")  # Debug print
            
            if data.get("cod") != "404":
                # Get current weather details
                current = data['list'][0]
                current_temp = current['main']['temp']
                current_condition = current['weather'][0]['main']
                humidity = current['main']['humidity']
                wind_speed = current['wind']['speed']
                
                # Format current weather
                current_text = f"Current Weather:\n"
                current_text += f"Temperature: {current_temp}°C\n"
                current_text += f"Condition: {current_condition}\n"
                current_text += f"Humidity: {humidity}%\n"
                current_text += f"Wind Speed: {wind_speed} m/s\n\n"
                
                # Process forecast data
                forecast_text = "5-Day Forecast:\n\n"
                for i in range(0, len(data['list']), 8):  # Get one forecast per day
                    forecast = data['list'][i]
                    date = forecast['dt_txt'].split()[0]
                    temp = forecast['main']['temp']
                    condition = forecast['weather'][0]['main']
                    forecast_text += f"{date}: {temp}°C, {condition}\n"
                
                # Update weather display with both sections
                self.weather_label.config(text=current_text + forecast_text)

                # Update weather effect
                self.update_weather_effect(current_condition)
            else:
                messagebox.showerror("Error", "City not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")
            
    def update_weather_effect(self, condition):
        # Clear previous effect
        if self.current_effect:
            for obj in self.current_effect.objects:
                self.canvas.delete(obj)
            self.current_effect = None
            
        # Create new effect based on condition
        condition_lower = condition.lower()
        if "rain" in condition_lower:
            self.current_effect = RainEffect(self.canvas)
        elif "snow" in condition_lower:
            self.current_effect = SnowEffect(self.canvas)
        elif "clear" in condition_lower:
            self.current_effect = SunEffect(self.canvas)
        elif "cloud" in condition_lower:
            self.current_effect = CloudEffect(self.canvas)
        elif "haze" in condition_lower or "mist" in condition_lower:
            self.current_effect = HazeEffect(self.canvas)

        # Start animation
        self.animate()
        
    def animate(self):
        if self.current_effect:
            self.current_effect.update()
        self.root.after(30, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
