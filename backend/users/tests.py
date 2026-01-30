from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import UserProfile, UserActivity


class UserModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
    
    def test_create_user(self):
        user = self.User.objects.create_user(
            phone_number='+2348012345678',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )
        self.assertEqual(user.phone_number, '+2348012345678')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.full_name, 'John Doe')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
    
    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            phone_number='+2348098765432',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpass123'
        )
        self.assertEqual(admin_user.phone_number, '+2348098765432')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_risk_level_calculation(self):
        user = self.User.objects.create_user(
            phone_number='+2348011111111',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
        user.soro_score = 25
        self.assertEqual(user.risk_level, 'low')
        
        user.soro_score = 50
        self.assertEqual(user.risk_level, 'medium')
        
        user.soro_score = 85
        self.assertEqual(user.risk_level, 'high')


class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()
        
        # Create test users
        self.admin_user = self.User.objects.create_superuser(
            phone_number='+2348012345678',
            email='admin@soro.com',
            first_name='Admin',
            last_name='User',
            password='admin123',
            user_type='admin'
        )
        
        self.customer_user = self.User.objects.create_user(
            phone_number='+2348098765432',
            email='customer@soro.com',
            first_name='Customer',
            last_name='User',
            password='customer123',
            user_type='customer'
        )
    
    def test_user_registration(self):
        url = '/api/users/register/'
        data = {
            'phone_number': '+2348033333333',
            'email': 'newuser@soro.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'password2': 'newpass123',
            'user_type': 'customer'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Verify user was created
        user = self.User.objects.get(phone_number='+2348033333333')
        self.assertEqual(user.email, 'newuser@soro.com')
        
        # Verify profile was created
        self.assertTrue(hasattr(user, 'profile'))
    
    def test_user_login(self):
        url = '/api/users/login/'
        data = {
            'phone_number': '+2348098765432',
            'password': 'customer123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_get_current_user(self):
        self.client.force_authenticate(user=self.customer_user)
        url = '/api/users/me/'
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '+2348098765432')
        self.assertEqual(response.data['user_type'], 'customer')
    
    def test_update_profile(self):
        self.client.force_authenticate(user=self.customer_user)
        url = '/api/users/update_profile/'
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'address': '123 Test Street, Lagos'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify updates
        self.customer_user.refresh_from_db()
        self.assertEqual(self.customer_user.first_name, 'Updated')
        self.assertEqual(self.customer_user.last_name, 'Name')
        self.assertEqual(self.customer_user.address, '123 Test Street, Lagos')
    
    def test_admin_update_soro_score(self):
        self.client.force_authenticate(user=self.admin_user)
        url = f'/api/users/admin/users/{self.customer_user.id}/update_soro_score/'
        data = {'soro_score': 75.5}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify update
        self.customer_user.refresh_from_db()
        self.assertEqual(self.customer_user.soro_score, 75.5)
        self.assertEqual(self.customer_user.risk_level, 'high')