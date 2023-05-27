from django.shortcuts import render
import datetime
# import matplotlib.pyplot as plt
# import os
# Create your views here.

def home(request):
    import json
    import requests

    if request.method == "POST":
        input = request.POST['input']
        # for char in city:
        #     if char.isdigit():
        #         return render(request, 'home.html', {'api':"Error..."})

        def check_level(oz_level):
            if 0<oz_level<=50:
                return "good"
            elif 50<oz_level<=100:
                return "fair"
            elif 100<oz_level<=130:
                return "moderate"
            elif 130<oz_level<=240:
                return "poor"
            elif 240<oz_level<=380:
                return "very poor"
        
        try:
            loc_api_req = requests.get(f"https://geocode.maps.co/search?q={input}")
            loc_api = json.loads(loc_api_req.content)
            lat, lon = loc_api[0]['lat'], loc_api[0]['lon']
            location = loc_api[0]['display_name'].split(',', 1)
            loc_1, loc_2 = location[0], location[1]
            print(f"Lattitude is {lat} and Longitude is {lon} for {location}")
            ozone_api_req = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=ozone&domains=cams_global")
            oz_api = json.loads(ozone_api_req.content)
            date = oz_api['hourly']['time']
            ozone = oz_api['hourly']['ozone']
            unit = oz_api['hourly_units']['ozone']

            date_list = [datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M') for string in date]

            # fig = plt.figure()
            # ax = fig.add_subplot(111)
            # ax.plot(date_list, ozone)
            # plt.xlabel('Date')
            # plt.ylabel('Value')
            # plt.title('Line plot example')
            # plt.savefig('img/line_chart.png')

            current_hour = datetime.datetime.now().hour
            oz_level = ozone[current_hour]
            print(f"Current Hour is {current_hour} thus date and ozone are {date_list[current_hour]} and {oz_level} respectively.")


        except Exception as e:
            oz_level = "Error..."
        return render(request, 'home.html', {'api':oz_level, 'unit':unit, 'air_qual':check_level(oz_level), 'city': loc_1, 'street':loc_2})

    else:
        return render(request, 'home.html')

def about(request):
    return render(request, 'about.html', {})