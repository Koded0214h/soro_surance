from django.test import TestCase
from django.contrib.auth import get_user_model

class NewUserModelTests(TestCase):
    def test_create_user_new(self):
        User = get_user_model()
        user = User.objects.create_user(
            phone_number='+2348012345679',
            email='testnew@example.com',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )
        self.assertEqual(user.phone_number, '+2348012345679')
