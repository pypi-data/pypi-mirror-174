from beanie import Document, Indexed, Link
from typing import List


class Event(Document):
    year: Indexed(int)
    session: Indexed(str)
    round: Indexed(str)


class Lap(Document):
    lap_time: Indexed(float)
    driver_number: int
    driver: Indexed(str)
    lap_number: int
    sector_1_time: float
    sector_2_time: float
    sector_3_time: float
    compound: str
    event: Link[Event]


class Telemetry(Document):
    rpm: int
    speed: float
    gear: int
    throttle: int
    brake: bool
    drs: int
    time: float
    distance: float
    lap: Link[Lap]
    event: Link[Event]
