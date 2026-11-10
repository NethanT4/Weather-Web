
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import City
from .forms import CityForm

load_dotenv(Path(settings.BASE_DIR) / '.env', override=True)


def index(request):
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    print("BASE DIR:", settings.BASE_DIR)
    print("ENV FILE EXISTS:", (Path(settings.BASE_DIR) / '.env').exists())
    print("API KEY LOADED:", bool(API_KEY))
    print("API KEY LENGTH:", len(API_KEY) if API_KEY else 0)

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            city_name = form.cleaned_data['name'].strip()

            # Check if city already exists
            city_exists = City.objects.filter(
                name__iexact=city_name
            ).exists()

            # Save only if city doesn't exist
            if not city_exists:
                City.objects.create(name=city_name)

            # Prevent form resubmission
            return redirect('index')

    else:
        form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:

        url = 'https://api.openweathermap.org/data/2.5/weather'

        try:
            response = requests.get(
                url,
                params={
                    'q': city.name,
                    'units': 'metric',
                    'appid': API_KEY
                },
                timeout=10
            )

            r = response.json()

        except requests.RequestException as e:
            print(f"Request error for {city.name}: {e}")
            continue

        if r.get('cod') != 200:
            print(f"Error for {city.name}: {r.get('message')}")
            continue

        city_weather = {
            'id': city.id,
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



@require_POST
def delete_city(_request, city_id):
    city = get_object_or_404(City, id=city_id)
    city.delete()

    return redirect('index')
