from pydantic import BaseModel, validator, Field
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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
