import paho.mqtt.client as mqtt

CLIENT_ID = 'test'
USER = 'test'
PASS = 'test'
IP = 'test'
PORT = 8883

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.tls_set()
client.username_pw_set(USER, password=PASS)
client.connect(IP, PORT, 60)
