# mqtt-vehicle-tracker

Attivazione dell'ambiente virtuale:
Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate

Installa le dipendenze:

pip install -r requirements.txt


# MQTT Dashboard Project

## Project Overview
This project is designed to receive real-time data from an MQTT broker, store it in a PostgreSQL database using Tortoise ORM, and expose the data through a FastAPI application for future dashboard visualization.

## Setup Instructions

### Clone the Repository
Clone this repository to your local machine.

### Docker Setup
Ensure Docker and Docker Compose are installed on your system.

### Run the Project
To start the project, run the following command in the root directory:

```bash
docker-compose up --build
