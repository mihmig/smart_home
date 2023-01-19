from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import json


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
    datetime: Optional[datetime]
    last_record_id: Optional[int]
    current: Optional[float]
    energy: Optional[float]
    power: Optional[int]
    voltage: Optional[int]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
