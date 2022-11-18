from pydantic import BaseModel, validator, Field
from typing import Optional


class Event(BaseModel):
    battery: Optional[float]
    battery_low: Optional[bool]
    contact: Optional[bool]
    linkquality: Optional[int]
    voltage: Optional[int]
    temperature: Optional[float]
    humidity: Optional[float]
    illuminance_lux: Optional[int]
    action: Optional[str]
    state: Optional[str]
    power_on_behavior: Optional[str]
    switch_type: Optional[str]
