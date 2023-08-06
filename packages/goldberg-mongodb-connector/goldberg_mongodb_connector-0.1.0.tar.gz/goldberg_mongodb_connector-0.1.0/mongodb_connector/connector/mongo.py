from ..models import Event, Lap, Telemetry
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import logging


async def connect_mongo_client(url: str):
    """Connect to the MongoDB server."""
    logging.info(f"Connecting to MongoDB {url}...")
    client = AsyncIOMotorClient(url)
    await init_beanie(database=client.db_name, document_models=[Event, Lap, Telemetry])
    logging.info("Connected to MongoDB")
