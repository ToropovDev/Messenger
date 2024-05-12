from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    user_1: int
    user_2: int
    by: int
    text: str
    time: datetime
