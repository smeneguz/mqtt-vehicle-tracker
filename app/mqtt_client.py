import json
from paho.mqtt import client as mqtt_client
from models import VehicleData
from tortoise.transactions import in_transaction
from dotenv import load_dotenv

load_dotenv()  # Carica le variabili d'ambiente da .env

broker = os.getenv('MQTT_BROKER_URL')
port = int(os.getenv('MQTT_BROKER_PORT'))
topic = os.getenv('MQTT_TOPIC')
username = os.getenv('MQTT_USERNAME')
password = os.getenv('MQTT_PASSWORD')

# Callback function called when the client successfully connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

# Callback function called when a new message is received
async def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    # Use a transaction to ensure atomicity when creating the VehicleData object
    async with in_transaction() as connection:
        await VehicleData.create(data=data, using_db=connection)

# Function to start the MQTT client
def start_mqtt_client():
    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker and start the client loop
    client.connect(broker, port, 60)
    client.loop_start()