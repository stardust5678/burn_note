from datetime import datetime, timedelta, timezone
import uuid, hashlib

from api.db import SessionDep
from api.models import SecretMessage

class SecretMessageService():
    def __init__(self, session):
        self.session = session

    async def get_secret(self, token):
        try:
            secret = await self.session.get(SecretMessage, token)
            if secret is None:
                return None
        except SecretMessage.DoesNotExist: # TODO
            return None
        
        if secret.expires_at < datetime.now(timezone.utc):
            await self.delete_secret(token, secret)
            return None
        
        return secret.encrypted_message

    async def save_secret(self, encrypted_message):
        token = self.__generate_token()

        try:
            secret = SecretMessage(token=token, encrypted_message=encrypted_message)
            self.session.add(secret)
            await self.session.commit()
            await self.session.refresh(secret)
            return secret.token
        except Exception as e:
            # Handle logging error
            print(f"Error saving secret: {e}")
            raise

    async def delete_secret(self, token, secret=None):
        try:
            if secret is None:
                secret = await self.session.get(SecretMessage, token)
            await self.session.delete(secret)
            await self.session.commit()
        except SecretMessage.DoesNotExist: # TODO
            return False
        except Exception as e:
            # Handle logging error
            print(f"Error deleting secret: {e}")
            raise
        return True


    def __generate_token(self):
        unique_id = uuid.uuid4()
        token = hashlib.shake_256(str(unique_id).encode("UTF-8")).hexdigest(5)

        return token