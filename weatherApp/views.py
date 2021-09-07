from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=ae091eb47d31f3860ad775f8cf242c29'
    weather_data = []

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']

            city_exists = City.objects.filter(name=new_city).exists()

            if city_exists:
                city = City.objects.get(name=new_city)

                response = requests.get(url.format(city)).json()

                city_weather = {
                    'city': city.name,
                    'temperature': response['main']['temp'] ,
                    'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon'],
                }
                weather_data.append(city_weather)
                # print(city_weather)
            else:
                form.save()


    form = CityForm() # everytime form will restarted 

    # cities = City.objects.all()

    context = {
        'weather_data': weather_data,
        'form':form,
    }

    return render(request, 'weatherApp/weather.html',context)
    