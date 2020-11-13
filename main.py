'''
Neopixel matrix light!!
'''
import json
import time

import paho.mqtt.client as mqtt
import yaml

from simulator_output import SimulatorOutput

from colorable_effect_base import ColorableEffectBase

from effects.solid_color_effect import SolidColorEffect
from effects.pulse_color_effect import PulseColorEffect
from effects.ink_effect import InkEffect
from effects.gradient_color_effect import GradientColorEffect
from effects.horizontal_gradient_color_effect import HorizontalGradientColorEffect
from effects.rainbow_gradient_effect import RainbowGradientEffect
from effects.horizontal_rainbow_gradient_effect import HorizontalRainbowGradientEffect

# Load configuration

with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

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

state = {
    'state': False,
    'brightness': 1,
    'effect': 'solid',
    'color': (255, 255, 255),
}

# Light stuff
output = SimulatorOutput(rows = ROWS, cols = COLS)

effects = {
    'solid': SolidColorEffect(ROWS, COLS, color=(255, 0, 255)),
    'pulse': PulseColorEffect(ROWS, COLS, speed=0.005, points=[
        (0.0, 0.0), (0.42, 0.0), (0.58, 1.0), (1.0, 1.0)
    ], color=(255, 0, 255)),
    'ink': InkEffect(ROWS, COLS, speed=0.1),
    'gradient_color': GradientColorEffect(ROWS, COLS, color=(255, 0, 255), speed=0.1, angle=45, width=15),
    'rainbow_gradient': RainbowGradientEffect(ROWS, COLS, colors=[
        (228, 3, 3),(255, 140, 0), (255, 237, 0), (0, 219, 66), (0, 77, 255), (209, 0, 181),
    ], speed=0.1, angle=45, width=15),
    'horizontal_gradient_color': HorizontalGradientColorEffect(ROWS, COLS, color=(255, 0, 255), speed=0.1, width=3),
    'horizontal_rainbow_gradient': HorizontalRainbowGradientEffect(ROWS, COLS, colors=[
        (228, 3, 3),(255, 140, 0), (255, 237, 0), (0, 219, 66), (0, 77, 255), (209, 0, 181),
    ], speed=-0.1, width=3),
}
off_effect = SolidColorEffect(ROWS, COLS, color=(0, 0, 0))

queued_updates = {}

# MQTT stuff
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(COMMAND_TOPIC)
    client.publish(AVAILABLITY_TOPIC, 'online', qos=1, retain=False)
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
            if 'state' in message_json:
                new_state = message_json['state']
                if new_state == 'ON':
                    queued_updates['state'] = True
                else:
                    queued_updates['state'] = False
            if 'brightness' in message_json:
                new_brightness = message_json['brightness']
                queued_updates['brightness'] = new_brightness / 255.0
                print(new_brightness, queued_updates['brightness'])
            if 'effect' in message_json:
                new_effect = message_json['effect']
                queued_updates['effect'] = new_effect
            if 'color' in message_json:
                new_color = message_json['color']
                if 'r' in new_color and 'g' in new_color and 'b' in new_color:
                    queued_updates['color'] = (
                        new_color['r'], new_color['g'], new_color['b'],
                    )

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

        client.publish(STATE_TOPIC, json.dumps(state_update), qos=1, retain=False)
        queued_updates = {}

    try:
        effect = effects[state['effect']]
    except KeyError:
        effect = effects['solid']

    if isinstance(effect, ColorableEffectBase):
        effect.change_color(state['color'])

    # if light is on
    if state['state']:
        effect.evolve()
        data = effect.get_data(brightness=state['brightness'])
    else:
        data = off_effect.get_data()

    try:
        successful_draw = output.write(data) # pylint: disable=invalid-name
    except Exception as e:
        print(e)
        successful_draw = False # pylint: disable=invalid-name

    time.sleep(0.01)

client.publish(AVAILABLITY_TOPIC, 'offline', qos=1, retain=False)
client.loop_stop()
