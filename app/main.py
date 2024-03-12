from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from mqtt_client import start_mqtt_client

load_dotenv()  # Carica le variabili d'ambiente da .env

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    start_mqtt_client()
    print("MQTT client started.")

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