import requests
from django.shortcuts import render

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e1b1883d70029ea9e99e8203164db88b'

    # to change the city  
    city = 'Dubai'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city' : city,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
    }

    context = {'city_weather' : city_weather}
    print(city_weather)

    return render(request, 'weather/weather.html', context)

