from datetime import datetime

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column

from backend.src.auth.models import user

metadata = MetaData()

message = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_1", Integer, ForeignKey(user.c.id), nullable=False),
    Column("user_2", Integer, ForeignKey(user.c.id), nullable=False),
    Column("by", Integer, ForeignKey(user.c.id), nullable=False),
    Column("text", String, nullable=False),
    Column("time", TIMESTAMP, nullable=False, default=datetime.utcnow),
)










