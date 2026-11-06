import requests
from django.shortcuts import render
from .models import City

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e1b1883d70029ea9e99e8203164db88b'

    # to change the city  
    #city = 'Tokyo'

    cities = City.objects.all()

    weather_data = []

    for city in cities :

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    print(weather_data)

    context = {'weather_data' : weather_data}
    return render(request, 'weather/weather.html', context)

