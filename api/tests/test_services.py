import pytest
from datetime import datetime, timedelta, timezone

from api.models import SecretMessage
from api.services import SecretMessageService

class MockSession:
    def __init__(self):
        self._db = {}

    async def get(self, _, token):
        return self._db.get(token)

    def add(self, instance):
        self._db[instance.token] = instance

    async def commit(self):
        pass

    async def refresh(self, _):
        pass

    async def delete(self, instance):
        token = instance.token
        if token in self._db:
            del self._db[token]

@pytest.mark.asyncio
async def test_save_and_get_secret():
    session = MockSession()
    service = SecretMessageService(session)

    token = await service.save_secret("mock_encrypted_message")
    assert token in session._db

    secret_value = await service.get_secret(token)
    assert secret_value == "mock_encrypted_message"

@pytest.mark.asyncio
async def test_expired_secret():
    session = MockSession()
    token = "mock_token"
    secret = SecretMessage(
        token=token,
        encrypted_message="mock_encrypted_message",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1)
    )
    session._db[token] = secret

    service = SecretMessageService(session)
    result = await service.get_secret(token)
    assert result is None
    assert token not in session._db

@pytest.mark.asyncio
async def test_delete_secret():
    session = MockSession()
    token = "mock_token"
    secret = SecretMessage(
        token=token,
        encrypted_message="mock_encrypted_message",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )
    session._db[token] = secret

    service = SecretMessageService(session)
    result = await service.delete_secret(token)
    assert result is True
    assert token not in session._db
