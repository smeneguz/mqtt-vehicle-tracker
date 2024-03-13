from fastapi import FastAPI
import os
from tortoise.contrib.fastapi import register_tortoise
from mqtt_client import start_mqtt_client  # Aggiusta il percorso in base alla tua struttura

app = FastAPI()

async def startup_event():
    print("Starting MQTT client...")
    await start_mqtt_client()  # Assuming start_mqtt_client is an async function
    print("MQTT client started.")

async def shutdown_event():
    # If you need to do something on shutdown, add code here
    pass

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

db_url = os.getenv('DATABASE_URL')
register_tortoise(
    app,
    db_url=db_url,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
# Endpoint di base
@app.get("/")
async def read_root():
    return {"Hello": "World"}
