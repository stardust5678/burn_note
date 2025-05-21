from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from app import service
from app.models import SecretMessage

class SecretMessageTestCase(TestCase):
    def setUp(self):
        self.token = "mockToken12345"
        self.encrypted_message = "mockAkln25p9r8oiawefkjn34982oi3rhkjwefn"

    def set_up_secret_message(self, expires_at=None):
        secret = SecretMessage.objects.create(
            token=self.token,
            encrypted_message=self.encrypted_message,
            expires_at= expires_at if expires_at else timezone.now() + timedelta(hours=24)
        )
        return secret
    
    def tearDown(self):
        SecretMessage.objects.all().delete()

    def test_get_secret_is_not_none(self):
        self.set_up_secret_message()
        result = service.get_secret(self.token)
        self.assertIsNotNone(result)

    def test_get_secret_is_none(self):
        self.set_up_secret_message()
        result = service.get_secret("nonExistentToken")
        self.assertIsNone(result)

    def test_get_secret_expired(self):
        expired_time = timezone.now() - timedelta(days=1)
        self.set_up_secret_message(expires_at=expired_time)
        result = service.get_secret(self.token)
        self.assertIsNone(result)

    def test_save_secret(self):
        token = service.save_secret(self.encrypted_message)
        self.assertIsNotNone(token)

    @patch("app.service.save_secret", side_effect=Exception("fail"))
    def test_save_secret_raises_exception(self, mock_save):
        self.set_up_secret_message()
        with self.assertRaises(Exception):
            mock_save(self.token)

    def test_delete_secret_with_token(self):
        self.set_up_secret_message()
        result = service.delete_secret(self.token)
        self.assertTrue(result)

    def test_delete_secret_with_object(self):
        secret = self.set_up_secret_message()
        result = service.delete_secret(self.token, secret)
        self.assertTrue(result)
    
    def test_delete_secret_not_found(self):
        self.set_up_secret_message()
        result = service.delete_secret("nonExistentToken")
        self.assertFalse(result)

    @patch("app.service.delete_secret", side_effect=Exception("fail"))
    def test_delete_secret_raises_exception(self, mock_delete):
        self.set_up_secret_message()
        with self.assertRaises(Exception):
            mock_delete(self.token)
