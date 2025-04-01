from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class Event(BaseModel):

    model_config = ConfigDict(
        frozen = True
    )

    event_type: str
    source: str
    event_id: str = Field(default_factory=lambda: uuid4())
    timestamp: datetime = Field(default=datetime.now())
