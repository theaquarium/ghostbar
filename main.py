'''
Neopixel matrix light!!
'''
import json
import time

import paho.mqtt.client as mqtt
import os
import yaml

# from neopixel_output import *
from simulator_output import SimulatorOutput

from colorable_effect_base import ColorableEffectBase

from effects.solid_color_effect import SolidColorEffect
from effects.pulse_color_effect import PulseColorEffect
from effects.ink_effect import InkEffect
from effects.gradient_color_effect import GradientColorEffect
from effects.horizontal_gradient_color_effect import HorizontalGradientColorEffect
from effects.rainbow_gradient_effect import RainbowGradientEffect
from effects.horizontal_rainbow_gradient_effect import HorizontalRainbowGradientEffect
from effects.rain_effect import RainEffect
from effects.fireworks_effect import FireworksEffect
from effects.stars_effect import StarsEffect
from effects.pride_progress_effect import PrideProgressEffect

# Load configuration
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, 'config.yaml')) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

DELAY = config['delay']
ROWS = config['rows']
COLS = config['columns']
CLIENT_ID = config['mqtt_client_id']
USER = config['mqtt_username']
PASS = config['mqtt_password']
IP = config['mqtt_broker_address']
PORT = config['mqtt_broker_port']
COMMAND_TOPIC = config['mqtt_command_topic']
STATE_TOPIC = config['mqtt_state_topic']
AVAILABLITY_TOPIC = config['mqtt_availability_topic']

# Build state object
state = {}
state['state'] = config['default_state']['state']
state['brightness'] = config['default_state']['brightness']
state['effect'] = config['default_state']['effect']
state['color'] = (
    config['default_state']['color'][0],
    config['default_state']['color'][1],
    config['default_state']['color'][2],
)

# Light stuff
output = SimulatorOutput(rows=ROWS, cols=COLS)
# output = NeopixelOutput(pixel_info=PixelInfo(pin='D18', order='GRB', brightness=1), rows = ROWS, cols = COLS, max_amps=15)

effects = {
    'solid': SolidColorEffect(ROWS, COLS, color=(255, 0, 255)),
    'pulse': PulseColorEffect(ROWS, COLS, speed=0.005, points=[
        (0.0, 0.0), (0.42, 0.0), (0.58, 1.0), (1.0, 1.0)
    ], color=(255, 0, 255)),
    'ink': InkEffect(ROWS, COLS, speed=0.5),
    'gradient_color': GradientColorEffect(ROWS, COLS, color=(255, 0, 255), speed=0.3, angle=45, width=15),
    'rainbow_gradient': RainbowGradientEffect(ROWS, COLS, colors=[
        (228, 3, 3),(255, 140, 0), (255, 237, 0), (0, 219, 66), (0, 77, 255), (209, 0, 181),
    ], speed=0.3, angle=45, width=15),
    'horizontal_gradient_color': HorizontalGradientColorEffect(ROWS, COLS, color=(255, 0, 255), speed=0.3, width=3),
    'horizontal_rainbow_gradient': HorizontalRainbowGradientEffect(ROWS, COLS, colors=[
        (228, 3, 3),(255, 140, 0), (255, 237, 0), (0, 219, 66), (0, 77, 255), (209, 0, 181),
    ], speed=-0.1, width=3),
    'rain': RainEffect(ROWS, COLS, color=(255, 0, 255), particle_color=(255, 255, 255), speed=0.1, density=30),
    'fireworks': FireworksEffect(ROWS, COLS, speed=0.1, density=5),
    'stars': StarsEffect(ROWS, COLS, color=(255, 0, 255), particle_color=(255, 255, 255), points=[
        (0.0, 0.0), (0.42, 0.0), (0.58, 1.0), (1.0, 1.0)
    ], speed=0.015, density=10),
    'pride_progress': PrideProgressEffect(ROWS, COLS, background_colors=[
        (228, 3, 3),(255, 140, 0), (255, 237, 0), (0, 219, 66), (0, 77, 255), (209, 0, 181),
    ], chevron_colors=[
        (255, 255, 255), (255, 175, 200), (116, 215, 236), (96, 56, 20), (0, 0, 0),
    ], speed=0.3, angle=45, width=15),
}
off_effect = SolidColorEffect(ROWS, COLS, color=(0, 0, 0))

queued_updates = {}
transition_effects = {}

# MQTT stuff
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(COMMAND_TOPIC)
    client.publish(AVAILABLITY_TOPIC, 'online', qos=1, retain=True)
    state_update = {
        'state': 'ON' if state['state'] else 'OFF',
        'brightness': state['brightness'] * 255,
        'effect': state['effect'],
        'color': {
            'r': state['color'][0],
            'g': state['color'][1],
            'b': state['color'][2],
        },
    }

    client.publish(STATE_TOPIC, json.dumps(state_update), qos=1, retain=False)

def on_message(client, userdata, msg):
    message_text = str(msg.payload.decode("utf-8"))
    print('received message on', msg.topic, message_text)
    if msg.topic == COMMAND_TOPIC:
        try:
            message_json = json.loads(message_text)
        except json.decoder.JSONDecodeError:
            print('invalid json received')
            return
        else:
            global transition_effects
            do_transition = False
            transition_effects = {}
            if 'transition' in message_json:
                do_transition = True
                transition_effects['old_color'] = state['color']
                transition_effects['old_brightness'] = state['brightness']
                transition_effects['duration'] = message_json['transition']
                transition_effects['start_time'] = time.time()
            if 'state' in message_json:
                new_state = message_json['state']
                if new_state == 'ON':
                    queued_updates['state'] = True
                    if do_transition and not state['state']:
                        transition_effects['old_brightness'] = 0
                        transition_effects['new_brightness'] = state['brightness']
                        transition_effects['new_state'] = True
                else:
                    queued_updates['state'] = False
                    if do_transition and state['state']:
                        transition_effects['old_brightness'] = state['brightness']
                        transition_effects['new_brightness'] = 0
                        transition_effects['new_state'] = False
            if 'brightness' in message_json:
                new_brightness = message_json['brightness']
                queued_updates['brightness'] = new_brightness / 255.0
                if do_transition:
                    transition_effects['new_brightness'] = queued_updates['brightness']
            if 'effect' in message_json:
                new_effect = message_json['effect']
                queued_updates['effect'] = new_effect
            if 'color' in message_json:
                new_color = message_json['color']
                if 'r' in new_color and 'g' in new_color and 'b' in new_color:
                    queued_updates['color'] = (
                        new_color['r'], new_color['g'], new_color['b'],
                    )
                    if do_transition:
                        transition_effects['new_color'] = queued_updates['color']
                        # if light is turning on with a color and state transition
                        # use new color as old color too so it doesn't fade from whatever was before
                        if 'new_state' in transition_effects:
                            transition_effects['old_color'] = queued_updates['color']

if config['use_mqtt']:
    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set()
    client.username_pw_set(USER, password=PASS)
    client.connect(IP, PORT, 60)

    # Start async MQTT loop
    client.loop_start()

# stupid stupid linter if someone wants to explain why this needs to be all caps go ahead
successful_draw = True # pylint: disable=invalid-name
while successful_draw:

    if config['use_mqtt'] and int(time.time()) % 30 == 0:
        client.publish(AVAILABLITY_TOPIC, 'online', qos=1, retain=True)

    if 'state' in queued_updates:
        state['state'] = queued_updates['state']
    if 'effect' in queued_updates:
        state['effect'] = queued_updates['effect']
    if 'brightness' in queued_updates:
        state['brightness'] = queued_updates['brightness']
    if 'color' in queued_updates:
        state['color'] = queued_updates['color']

    if len(queued_updates.keys()) > 0:
        state_update = {
            'state': 'ON' if state['state'] else 'OFF',
            'brightness': state['brightness'] * 255,
            'effect': state['effect'],
            'color': {
                'r': state['color'][0],
                'g': state['color'][1],
                'b': state['color'][2],
            },
        }

        if config['use_mqtt']:
            client.publish(STATE_TOPIC, json.dumps(state_update), qos=1, retain=False)
        queued_updates = {}

    try:
        effect = effects[state['effect']]
    except KeyError:
        effect = effects['solid']

    transition_color = state['color']
    transition_brightness = state['brightness']
    transition_state = state['state']
    if len(transition_effects.keys()) > 0:
        transition_ratio = (time.time() - transition_effects['start_time']) / transition_effects['duration']
        if 'new_brightness' in transition_effects:
            old_brightness = transition_effects['old_brightness']
            new_brightness = transition_effects['new_brightness']
            brightness_diff = new_brightness - old_brightness
            if transition_ratio > 1.0:
                transition_brightness = new_brightness
            else:
                transition_brightness = old_brightness + brightness_diff * transition_ratio
        if 'new_color' in transition_effects:
            old_col = transition_effects['old_color']
            new_col = transition_effects['new_color']
            r_diff = new_col[0] - old_col[0]
            g_diff = new_col[1] - old_col[1]
            b_diff = new_col[2] - old_col[2]
            if transition_ratio > 1.0:
                transition_color = new_col
            else:
                transition_color = (
                    old_col[0] + r_diff * transition_ratio,
                    old_col[1] + g_diff * transition_ratio,
                    old_col[2] + b_diff * transition_ratio,
                )
        if 'new_state' in transition_effects:
            transition_state = True
        if transition_ratio > 1:
            transition_effects = {}

    if isinstance(effect, ColorableEffectBase):
        effect.change_color(transition_color)

    # # if light is on
    # if state['state']:
    #     effect.evolve()
    #     data = effect.get_data(brightness=state['brightness'])
    # else:
    #     data = off_effect.get_data()

    # effect.evolve()
    # successful_draw = output.write(effect, brightness=transition_brightness)
    
    if config['catch_errors']:
        try:
            # if light is on
            if transition_state:
                effect.evolve()
                successful_draw = output.write(effect, brightness=transition_brightness) # pylint: disable=invalid-name
            else:
                successful_draw = output.write(off_effect, brightness=transition_brightness) # pylint: disable=invalid-name
            # successful_draw = output.write(data) # pylint: disable=invalid-name
        except Exception as e:
            print(e)
            successful_draw = False # pylint: disable=invalid-name
    else:
        if transition_state:
            effect.evolve()
            successful_draw = output.write(effect, brightness=transition_brightness) # pylint: disable=invalid-name
        else:
            successful_draw = output.write(off_effect, brightness=transition_brightness) # pylint: disable=invalid-name

    time.sleep(DELAY)

if config['use_mqtt']:
    client.publish(AVAILABLITY_TOPIC, 'offline', qos=1, retain=False)
    client.loop_stop()
