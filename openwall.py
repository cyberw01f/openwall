import json
import requests
import os
import subprocess
from datetime import date

parameters = {}
openwall_url = ""
wall_source = ""
wall_duration = ""
last_update = ''


def load_config(type: str):
    with open('openwall_config.json', 'r') as f:
        config = json.load(f)
        global parameters
        global openwall_url
        parameters.clear()
        if type == 'apod':
            nasa_url = config['nasa_params']['nasa_url']
            nasa_key = config['nasa_params']['api_key']
            hd = config['nasa_params']['hd']
            parameters = {
                'api_key': nasa_key,
                'hd': hd
            }
            openwall_url = nasa_url


def update_rules(source, duration):
    with open("openwall_config.json", "r") as f:
        data = json.load(f)
    data['settings']['source'] = source
    data['settings']['change_duration'] = duration
    jsonFile = open("openwall_config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
    main_menu()


def update_date(update_date):
    with open("openwall_config.json", "r") as f:
        data = json.load(f)
    data['settings']['update_date'] = str(update_date)
    jsonFile = open("openwall_config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()


def get_update_date():
    with open('openwall_config.json', 'r') as f:
        config = json.load(f)
        global last_update
        last_update = config['settings']['last_update']


def update_source_menu():
    global wall_source
    print("Enter the source number you would like to use:\n\n"
          "1. NASA APOD\n"
          "2. Unsplash\n"
          "3. Flickr\n"
          "4. Cancel and go back to main menu\n")
    while 1:
        task = input(">> ")
        if task == '1':     # NASA APOD
            wall_source = 'APOD'
            update_duration_menu()
            break
        elif task == '2':   # Unsplash
            wall_source = 'UNSPLASH'
            update_duration_menu()
            break
        elif task == '3':   # Flickr
            wall_source = 'FLICKR'
            update_duration_menu()
            break
        elif task == '4':   # Cancel
            main_menu()
            break
        else:
            print("woah there ! please stick to the menu item")


def update_duration_menu():
    global wall_duration
    print("Enter the source number you would like to use:\n\n"
          "1. Every Hour\n"
          "2. Every Day\n"
          "3. Cancel and go back to main menu\n")
    while 1:
        task = input(">> ")
        if task == '1':
            wall_duration = '60'
            update_rules(wall_source, wall_duration)
            break
        elif task == '2':
            wall_duration = '1440'
            update_rules(wall_source, wall_duration)
            break
        elif task == '3':
            main_menu()
            break
        else:
            print("woah there ! please stick to the menu item")


def main_menu():
    os.system('clear')
    print("-----------------------------------------------\n"
          "              Welcome to OpenWall\n"
          "-----------------------------------------------\n\n"
          "Enter the menu number to proceed\n\n"
          "1. Download and set NASA APOD\n"
          "2. Download and set random image from Unsplash\n"
          "3. Download and set random image from Flickr\n"
          "4. Set or edit rule for wallpaper rotation\n"
          "5. Exit\n\n"
          "-----------------------------------------------\n\n")
    while 1:
        task = input(">> ")
        if task == '1':     # Download and set NASA APOD
            open_wall('apod')
            break
        elif task == '2':   # Download and set random image from Unsplash
            print("Sorry, option under development")
        elif task == '3':   # Download and set random image from Flickr
            print("Sorry, option under development")
        elif task == '4':   # Set or edit rule for wallpaper rotation
            update_source_menu()
        elif task == '5':   # Exit
            os.system('clear')
            print("Thank you for using OpenWall")
            break
        else:
            print("woah there ! please stick to the menu item")


def set_wallpaper(wallpaper_file):
    try:
        subprocess.call(["feh", "--bg-fill", wallpaper_file])
    except OSError:
        pass
    try:
        subprocess.call(["nitrogen", "--set-zoom-fill", wallpaper_file])
    except OSError:
        pass


def todays_date():
    today = str(date.today())
    return today


def open_wall(type: str):
    load_config(type)
    pictures_folder = os.path.join(os.getenv('HOME'), 'Pictures')
    picture_name = 'openwall_' + type + '_' + todays_date() + '.jpg'
    image_file = os.path.join(pictures_folder, picture_name)

    r = requests.get(openwall_url, params=parameters)

    if (r.status_code == 200):
        data = json.loads(r.content.decode('utf-8'))
        if (data['media_type'] == "image"):
            print("Getting image from server")
            response = requests.get(data['hdurl'])
            print("Writing image to local disk, Please wait")
            with open(image_file, 'wb') as f:
                f.write(response.content)
            print("Image downloaded at location : " + pictures_folder)
            set_wallpaper(image_file)
            # update_date(todays_date())
            print("Wallpaper updated")
        else:
            print("There doesn't seem to be an image today !")

    elif (response.status_code == 429):
        print("Download error - You have made too many requests!")

    else:
        print("Download error - Could not download !")
        print(response.status_code)
        return None


main_menu()
