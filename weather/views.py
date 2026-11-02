import requests
from django.shortcuts import render

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e1b1883d70029ea9e99e8203164db88b'
    city = 'Las Vegas'

    r = requests.get(url.format(city))
    print(r.text)

    return render(request, 'weather/weather.html')

