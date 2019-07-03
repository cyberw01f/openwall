import json
import requests
import os
import sys
import time
import subprocess

nasa_url = 'https://api.nasa.gov/planetary/apod'
parameters = {
    'api_key': 'DEMO_KEY',
    'hd': 'True'
}

def user_menu():
    os.system('clear')
    print("---------------------------------\n"
            "       Welcome to OpenWall\n"
            "---------------------------------\n\n"
            "Enter the menu number to proceed\n\n"
            "1. Download and set NASA APOD\n"
            "2. Exit\n\n"
            "---------------------------------\n\n")
    while 1:
        task=input(">> ")
        if task=='1':
            nasa_APOD()
        elif task=='2':
            print("Thank you for using OpenWall")
            break
        else:
            print("woah there ! please stick to the menu item")


def set_wallpaper(wallpaper_file):
    try:
        feh = subprocess.call(["feh", "--bg-fill", wallpaper_file])
    except OSError:
        pass
    try:
        nitrogen = subprocess.call(["nitrogen", "--set-zoom-fill", wallpaper_file])
    except OSError:
        pass

def nasa_APOD():
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
            print("Downloaded at location : " + pictures_folder)
            set_wallpaper(image_file)
            print("Wallpaper updated")
        else:
            print("There doesn't seem to be an image today !")

    elif (response.status_code == 429):
        print("Download error - You have made too many requests!")

    else:
        print("Download error - Could not download !")
        print(response.status_code)
        return None

user_menu()
