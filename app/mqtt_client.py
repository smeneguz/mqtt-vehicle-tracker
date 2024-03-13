import asyncio
import json
from models import VehicleData
from tortoise.transactions import in_transaction
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import os
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()  # Carica le variabili d'ambiente da .env

broker = os.getenv('MQTT_BROKER_URL')
port = int(os.getenv('MQTT_BROKER_PORT'))
topic = os.getenv('MQTT_TOPIC')
username = os.getenv('MQTT_USERNAME')
password = os.getenv('MQTT_PASSWORD')


# Callback function called when the client successfully connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logging.info("Connected with result code " + str(rc))
        logging.info(f"sessionPresent: {flags}")

        
        client.subscribe(topic)

    else:
        logging.error("Connection failed with result code " + str(rc))


# Callback function called when a new message is received
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        logging.info(f"Received data: {data}")
        
        # Inoltra i dati a un'altra funzione che gestisce l'asincrono
        threading.Thread(target=asyncio.run, args=(process_message_async(data),)).start()

    except Exception as e:
        logging.error(f"Error processing message: {e}", exc_info=True)

async def process_message_async(data):
    try:
        # Utilizza una transazione per assicurare l'atomicità nella creazione dell'oggetto VehicleData
        async with in_transaction():
            await VehicleData.create(**data)
    except Exception as e:
        logging.error(f"Error saving data to database: {e}", exc_info=True)


# Function to start the MQTT client
async def start_mqtt_client():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username_pw_set(username, password)
    mqttc.on_connect = on_connect
    mqttc.message_callback_add(topic, on_message)

    try:
        test = mqttc.connect(broker, port, 60)
        logging.info(f"Connection code: {test}") # 0 = success, 1 = refused, 2 = unacceptable protocol, 3 = client id rejected, 4 = server unavailable, 5 = bad username or password, 6-255 = not authorized
        mqttc.subscribe(topic)
        mqttc.loop_start()
    except Exception as e:
        logging.error(f"Error starting MQTT client: {e}", exc_info=True)
        mqttc.loop_stop()


# Run the client asynchronously (assuming your application is set up for async)
# asyncio.create_task(start_mqtt_client())  # Example usage
