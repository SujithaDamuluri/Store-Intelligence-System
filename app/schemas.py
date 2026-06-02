from pydantic import BaseModel
from typing import Optional


class Event(BaseModel):
    event_type: str
    id_token: str
    store_code: str
    camera_id: str
    event_timestamp: str
    is_staff: bool = False