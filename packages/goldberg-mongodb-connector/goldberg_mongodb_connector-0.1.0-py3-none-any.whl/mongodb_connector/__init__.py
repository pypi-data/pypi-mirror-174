"""mongodb_connector"""

__version__ = "0.1.0"


from .models import Telemetry, Lap, Event

from .connector import connect_mongo_client


__all__ = ["Event", "Lap", "Telemetry"]  # import all class here
