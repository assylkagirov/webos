import requests
from django.shortcuts import render, redirect
from .models import CityModel
from .forms import CityForm
from django.http import HttpResponse
import json

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=28dd5a902028120311be7fc0569bc196'

    cities = CityModel.objects.order_by('-id')

    weather_data = []

    for city in cities:
        try:
            r = requests.get(url.format(city)).json()

            city_weather = {
                'id': city.id,
                'city': city.city,
                'temperature': r['main']['temp'],
                'humidity': r['main']['humidity'],
                'wind': r['wind']['speed'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],

            }
            weather_data.append(city_weather)
        except KeyError:
            city_weather = {
                'id': city.id,
                'city': "invalid city",

            }
            weather_data.append(city_weather)

        else:
            pass

    form = CityForm()

    context = {
        'weather_data': weather_data,
        'form': form
    }

    # Set cookie flag
    response = render(request, 'weather/weather.html', context)

    # Set the cookie value to "ты нашел флаг"
    response.set_cookie('thisisflagnumber2', 'congrats')

    return response


def addcity(request):
    form = CityForm(request.POST)

    if form.is_valid():
        city_name = request.POST['city']

        # Check if the city name contains the specified string
        if "<script>alert(xss)</script>" in city_name.lower():
            # Construct the response with JavaScript to trigger the alert
            response_data = {
                'message': 'This is flag number 3'
            }
            response = HttpResponse(json.dumps(response_data), content_type='application/json')
            return response

        if "cat ../settings.py" in city_name.lower():
            # Construct the response with JavaScript to trigger the alert
            response_data = {
                'message': 'This is flag number 4'
            }
            response = HttpResponse(json.dumps(response_data), content_type='application/json')
            return response


        new_city = CityModel(city=city_name)
        new_city.save()

    return redirect('index')



def delete(request, city_id):
    city = CityModel.objects.get(pk=city_id)
    city.delete()

    return redirect('index')
