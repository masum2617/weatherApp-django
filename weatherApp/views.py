from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=ae091eb47d31f3860ad775f8cf242c29'
    
    city = 'Dhaka'

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()


    form = CityForm() # everytime form will restarted 

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        response = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'] ,
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    # print(city_weather)

    context = {
        'weather_data': weather_data,
        'form':form,
    }

    return render(request, 'weatherApp/weather.html',context)
    