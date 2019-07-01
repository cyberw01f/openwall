import json
import requests
import os
import sys
import time

nasa_url = 'https://api.nasa.gov/planetary/apod'
parameters = {
    'api_key': 'DEMO_KEY',
    'hd': 'True'
}


def nasaAPOD():
    timestamp = time.time()
    pictures_folder = os.path.join(os.getenv('HOME'),'Pictures')
    picture_name = 'openwall_' + str(timestamp) + '.jpg'
    image_file = os.path.join(pictures_folder,picture_name)

    r = requests.get(nasa_url,params = parameters)

    if (r.status_code == 200):
        data = json.loads(r.content.decode('utf-8'))

        if (data['media_type'] == "image"):
            response = requests.get(data['hdurl'])
            open(image_file, 'wb').write(response.content)
            print ("Downloaded at location : " + pictures_folder)

    elif (response.status_code == 429):
        print   ("Download error - You have made too many requests!")

    else:
        print ("Download error - Could not download !")
        print (response.status_code)
        return None

nasaAPOD()
