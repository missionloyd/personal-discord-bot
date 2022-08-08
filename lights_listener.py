#assumes you have alrady set up groups within phillips hue app
from phue import Bridge
from dotenv import load_dotenv
import time, json, os
from datetime import datetime
from threading import Thread, Lock, Timer

bridge_ip = os.getenv('BRIDGE_IP')
b = Bridge(bridge_ip)

def display_status():
    light_groups_list = b.get_group()

    response = ""

    for group in light_groups_list:
        instance = light_groups_list[group]
        response += "\n" + instance['name'] + "\n"
        response += "Id: " + group + "\n"
        
        for light in instance['lights']:  
            light_info = b.get_light(int(light))['state']
            response += "Light: " + light + " ~ bri: " + str(light_info['bri']) + " hue: " + str(light_info['hue']) + " sat: " + str(light_info['sat']) + "\n"

        state = str(instance['state']).replace("True", "🌞").replace("False", "🌚")
        response += "State: " + state + "\n"

    return response

def set_lights(content):
    group = get_groupID(content)
    light_objects = b.get_light_objects('id')
    light_groups_list = b.get_group(group)

    for light in light_groups_list['lights']:
        light_id = int(light)
        light_objects[light_id].on = True
        light_objects[light_id].hue = 15000
        light_objects[light_id].saturation = 120

    return

def set_scene(content, emoji, themes, data, transition_time):
    group = get_groupID(content)
    light_groups_list = b.get_group(group)
    scene_name = ''
    for scene in data['scenes']:
        if(scene['emoji'] == emoji):
            scene_name = scene['name']
            break

    b.run_scene(light_groups_list['name'], scene_name, transition_time)

    return ""

def toggle_group(content):
    group = get_groupID(content)

    prev_status = b.get_group(group)['state']['all_on']
    b.set_group(group, 'on', not prev_status)
    next_status = b.get_group(group)['state']['all_on']
    response = ""

    if prev_status == next_status:
        response = "Error: "
    else:
        response = "Sucess: "

    if next_status is True:
        response += "Lights On"
    elif next_status is False:
        response += "Lights Off"
    else:
        response = "Error"
    
    return response

def get_groupID(content):
    group = -1

    if "Living Room" in content:
        group = 1
    elif "Luke's" in content:
        group = 2

    return group
    
# set_lights("Luke's")
# print(b.get_scene())

def display_scenes():
    for key, value in b.get_scene().items():
        print(value['name'])
    return


def strobe_alarm(count):
    # b.run_scene("Luke's Room", 'Bright', transition_time=0.2)
    time.sleep(1)
    toggle_group("Luke's")
    return

def check_time(time):

    now = datetime.now()
    current_time = now.strftime("%I:%M")
    print(current_time)

    # ex: '11:06'
    if(current_time == time):  # check if matches with the desired time
        return False
    
    return True

