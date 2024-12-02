import requests
from flask import Flask, render_template, request

app = Flask(__name__)


api_key = "9c557b50038e797c039e3ad6004eb6e7"


def get_weather(city):
    try:
        
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fr'
        
        # API
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()  
            main = data['main']
            weather = data['weather'][0]
            wind = data['wind']
            
            
            return {
                'temp': main['temp'],
                'description': weather['description'],
                'wind': wind['speed'],
                'humidity': main['humidity'],
                'city': city
            }
        else:
            print(f"Erreur avec la requête API (code {response.status_code}): {response.text}")
            return None
    except Exception as e:
        print(f"Erreur : {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = []
    cities = ["Paris", "New York", "Tokyo", "London", "Berlin", "Fès", "Casablanca"]  # Villes par défaut
    
    if request.method == "POST":
        city = request.form["city"]  
        if city:
            cities = [city]  

    
    for city in cities:
        city_weather = get_weather(city)
        if city_weather:
            weather_data.append(city_weather)
        else:
            weather_data.append({"city": city, "error": "Ville introuvable, essayez à nouveau."})
    
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
