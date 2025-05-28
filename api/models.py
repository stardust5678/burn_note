from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel

class SecretMessage(SQLModel, table=True):
    token: str = Field(primary_key=True, max_length=40)
    encrypted_message: str = Field(max_length=2048)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
        )
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=24),
        sa_column=Column(DateTime(timezone=True))
        )
