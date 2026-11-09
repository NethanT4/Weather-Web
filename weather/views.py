import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from django.conf import settings

from django.shortcuts import render
from .models import City
from .forms import CityForm

load_dotenv(Path(settings.BASE_DIR) / '.env')

def index(request):
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(
            city.name, API_KEY
        )

        r = requests.get(url).json()

        if r.get('cod') != 200:
            print(f"Error for {city.name}: {r.get('message')}")
            continue

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form
    }

    return render(request, 'weather/weather.html', context)
