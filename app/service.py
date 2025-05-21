from datetime import timedelta
import uuid, hashlib

from django.utils import timezone

from app.models import SecretMessage


def get_secret(token):
    try:
        secret = SecretMessage.objects.get(token=token)
    except SecretMessage.DoesNotExist:
        return None
    
    if secret.expires_at < timezone.now():
        secret.delete()
        return None
    
    return secret.encrypted_message

def save_secret(encrypted_message):
    token = __generate_token()

    try:
        secret = SecretMessage.objects.create(
            token=token,
            encrypted_message=encrypted_message,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        return secret.token
    except Exception as e:
        # Handle logging error
        print(f"Error saving secret: {e}")
        raise

def delete_secret(token, secret=None):
    try:
        if secret is None:
            secret = SecretMessage.objects.get(token=token)
        secret.delete()
    except SecretMessage.DoesNotExist:
        return False
    except Exception as e:
        # Handle logging error
        print(f"Error deleting secret: {e}")
        raise
    return True


def __generate_token():
    unique_id = uuid.uuid4()
    token = hashlib.shake_256(str(unique_id).encode("UTF-8")).hexdigest(5)

    return token

