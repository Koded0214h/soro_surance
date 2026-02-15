import json
import tempfile
from unittest.mock import patch, MagicMock, Mock
from datetime import date, timedelta
from decimal import Decimal
import speech_recognition as sr # Added import

from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.models import UserProfile
from .models import (
    InsuranceProduct, Policy, Claim, VoiceAnalysis,
    SoroScoreLog, Payment, Notification, AdminDashboard
)
from .serializers import (
    InsuranceProductSerializer, PolicySerializer, ClaimSerializer,
    PaymentSerializer, NotificationSerializer, AdminDashboardSerializer
)
from .services import (
    SoroScoreService, VoiceProcessingService,
    PaymentService, NotificationService, USSDService
)

User = get_user_model()


# ----------------------------------------------------------------------
# Helper factories to create test objects
# ----------------------------------------------------------------------
def create_user(phone_number='+2348000000000', **kwargs):
    user = User.objects.create_user(
        phone_number=phone_number,
        email=kwargs.get('email', f'{phone_number}@example.com'),
        first_name=kwargs.get('first_name', 'Test'),
        last_name=kwargs.get('last_name', 'User'),
        password=kwargs.get('password', 'testpass123'),
        user_type=kwargs.get('user_type', 'customer')
    )
    # Ensure profile exists (signal might not fire in tests)
    UserProfile.objects.get_or_create(user=user)
    return user


def create_product(**kwargs):
    defaults = {
        'name': 'Test Motor Insurance',
        'product_type': 'motor',
        'description': 'A test product',
        'base_premium': 10000.00,
        'min_premium': 5000.00,
        'max_premium': 50000.00,
        'coverage_details': {'max_coverage': 5000000, 'deductible': 5000},
        'exclusions': ['war', 'nuclear'],
        'required_documents': ['driver_license'],
        'is_active': True
    }
    defaults.update(kwargs)
    return InsuranceProduct.objects.create(**defaults)


def create_policy(user, product=None, **kwargs):
    if product is None:
        product = create_product()
    start_date = kwargs.get('start_date', date.today())
    end_date = kwargs.get('end_date', date.today() + timedelta(days=365))
    defaults = {
        'user': user,
        'product': product,
        'start_date': start_date,
        'end_date': end_date,
        'initial_soro_score': 50.0,
        'current_soro_score': 50.0,
        'premium_amount': product.base_premium,
        'coverage_amount': 5000000,
        'deductible_amount': 5000,
        'status': Policy.PolicyStatus.ACTIVE
    }
    defaults.update(kwargs)
    return Policy.objects.create(**defaults)


def create_claim(user, policy=None, **kwargs):
    if policy is None:
        policy = create_policy(user)
    defaults = {
        'policy': policy,
        'user': user,
        'claim_type': 'accident',
        'description': 'Test claim',
        'incident_date': date.today() - timedelta(days=2),
        'incident_location': 'Lagos, Nigeria',
        'estimated_loss': 50000.00,
        'claimed_amount': 45000.00,
        'status': Claim.ClaimStatus.DRAFT
    }
    defaults.update(kwargs)
    return Claim.objects.create(**defaults)


# ----------------------------------------------------------------------
# Model Tests
# ----------------------------------------------------------------------
class InsuranceProductModelTests(TestCase):
    def test_create_product(self):
        product = create_product()
        self.assertEqual(product.name, 'Test Motor Insurance')
        self.assertEqual(product.product_type, 'motor')
        self.assertTrue(product.is_active)
        self.assertEqual(str(product), "Test Motor Insurance (Motor Insurance)")


class PolicyModelTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.product = create_product()
        self.policy = create_policy(self.user, self.product)

    def test_policy_creation(self):
        # Refresh from DB to ensure UUID fields become strings
        self.policy.refresh_from_db()
        self.assertIsNotNone(self.policy.policy_number)
        self.assertIsInstance(self.policy.policy_number, str)
        self.assertEqual(self.policy.user, self.user)
        self.assertEqual(self.policy.product, self.product)
        self.assertTrue(self.policy.is_active)
        self.assertIsNotNone(self.policy.days_remaining)

    def test_policy_str(self):
        self.policy.refresh_from_db()
        expected = f"Policy {self.policy.policy_number} - Test User"
        self.assertEqual(str(self.policy), expected)


class ClaimModelTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.policy = create_policy(self.user)
        self.claim = create_claim(self.user, self.policy)

    def test_claim_creation(self):
        self.claim.refresh_from_db()
        self.assertIsNotNone(self.claim.claim_number)
        self.assertIsInstance(self.claim.claim_number, str)
        self.assertEqual(self.claim.user, self.user)
        self.assertEqual(self.claim.policy, self.policy)

    def test_claim_save_sets_risk_level(self):
        self.claim.soro_score = 25
        self.claim.save()
        self.assertEqual(self.claim.risk_level, 'low')

        self.claim.soro_score = 50
        self.claim.save()
        self.assertEqual(self.claim.risk_level, 'medium')

        self.claim.soro_score = 85
        self.claim.save()
        self.assertEqual(self.claim.risk_level, 'high')


class PaymentModelTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.payment = Payment.objects.create(
            user=self.user,
            payment_type='premium',
            amount=10000.00,
            currency='NGN',
            payment_gateway='paystack'
        )

    def test_payment_creation(self):
        self.payment.refresh_from_db()
        self.assertIsNotNone(self.payment.payment_reference)
        self.assertIsInstance(self.payment.payment_reference, str)
        self.assertEqual(self.payment.status, Payment.PaymentStatus.PENDING)


# ----------------------------------------------------------------------
# Serializer Tests
# ----------------------------------------------------------------------
class InsuranceProductSerializerTests(TestCase):
    def test_serializer(self):
        product = create_product()
        serializer = InsuranceProductSerializer(product)
        data = serializer.data
        self.assertEqual(data['name'], product.name)
        self.assertEqual(data['product_type'], product.product_type)


class PolicySerializerTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.product = create_product()
        self.policy = create_policy(self.user, self.product)

    def test_serializer(self):
        serializer = PolicySerializer(self.policy)
        self.assertEqual(serializer.data['user_name'], self.user.get_full_name())
        self.assertEqual(serializer.data['product_name'], self.product.name)
        self.assertIn('is_active', serializer.data)

    def test_create_policy_serializer(self):
        data = {
            'product': self.product.id,
            'start_date': date.today().isoformat(),
            'end_date': (date.today() + timedelta(days=365)).isoformat(),
        }
        request = MagicMock()
        request.user = self.user
        serializer = PolicySerializer(data=data, context={'request': request})
        # The serializer requires initial_soro_score etc., but we'll let the view set them.
        # In this unit test, we need to either provide them or mark them as read_only.
        # Since we are testing the serializer alone, we include dummy values.
        # Alternatively, we can update the serializer to make them optional (see required fix).
        self.assertTrue(serializer.is_valid(), serializer.errors)
        policy = serializer.save(
            user=self.user,  # pass user explicitly because it's required
            initial_soro_score=50.0,
            current_soro_score=50.0,
            premium_amount=self.product.base_premium,
            coverage_amount=1000000,
            deductible_amount=5000
        )
        self.assertEqual(policy.user, self.user)
        self.assertIsNotNone(policy.policy_number)


class ClaimSerializerTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.policy = create_policy(self.user)
        self.claim = create_claim(self.user, self.policy)

    def test_serializer(self):
        serializer = ClaimSerializer(self.claim)
        self.assertEqual(serializer.data['user_name'], self.user.get_full_name())
        # policy_number is a UUID string after refresh
        self.claim.refresh_from_db()
        self.policy.refresh_from_db()
        self.assertEqual(str(serializer.data['policy_number']), str(self.policy.policy_number))

    def test_create_with_audio(self):
        audio_file = SimpleUploadedFile("test.wav", b"fake audio data", content_type="audio/wav")
        data = {
            'policy': self.policy.id,
            'claim_type': 'accident',
            'incident_date': date.today().isoformat(),
            'incident_location': 'Lagos',
            'estimated_loss': 10000,
            'claimed_amount': 9000,
            'description': 'Test claim description',
            'audio_file': audio_file
        }
        request = MagicMock()
        request.user = self.user
        serializer = ClaimSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        claim = serializer.save(user=self.user)
        self.assertIsNotNone(claim.audio_file)


# ----------------------------------------------------------------------
# View Tests (APITestCase)
# ----------------------------------------------------------------------
class InsuranceProductViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = create_product()
        self.url = reverse('product-list')

    def test_list_products_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # If pagination is enabled, results are in response.data['results']
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_calculate_premium(self):
        url = reverse('product-calculate-premium', args=[self.product.id])
        data = {'soro_score': 30}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('calculated_premium', response.data)
        self.assertLess(response.data['calculated_premium'], float(self.product.base_premium))


class PolicyViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(phone_number='+2348011111111')
        self.admin = create_user(phone_number='+2348022222222', user_type='admin')
        self.product = create_product()
        self.policy = create_policy(self.user, self.product)
        self.client.force_authenticate(user=self.user)

    def test_list_policies_customer(self):
        url = reverse('policy-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_list_policies_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('policy-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_create_policy(self):
        url = reverse('policy-list')
        data = {
            'product': self.product.id,
            'start_date': date.today().isoformat(),
            'end_date': (date.today() + timedelta(days=365)).isoformat(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertIsNotNone(response.data['policy_number'])

    def test_retrieve_policy(self):
        url = reverse('policy-detail', args=[self.policy.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.policy.id)

    def test_claims_action(self):
        create_claim(self.user, self.policy)
        url = reverse('policy-claims', args=[self.policy.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_renew_policy(self):
        url = reverse('policy-renew', args=[self.policy.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('new_policy', response.data)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.status, Policy.PolicyStatus.EXPIRED)


class ClaimViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(phone_number='+2348011111111')
        self.admin = create_user(phone_number='+2348022222222', user_type='admin')
        self.product = create_product()
        self.policy = create_policy(self.user, self.product)
        self.claim = create_claim(self.user, self.policy)
        self.client.force_authenticate(user=self.user)

    def test_create_claim(self):
        url = reverse('claim-list')
        data = {
            'policy': self.policy.id,
            'claim_type': 'theft',
            'incident_date': date.today().isoformat(),
            'incident_time': '12:00:00',
            'incident_location': 'Lagos',
            'estimated_loss': 50000,
            'claimed_amount': 45000,
            'description': 'Test claim description',   # required field
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertIsNotNone(response.data['claim_number'])

    @patch('api.views.VoiceProcessingService')
    @patch('api.views.SoroScoreService')
    def test_submit_voice_claim(self, mock_soro_service, mock_voice_service):
        # Mock services
        mock_voice_instance = mock_voice_service.return_value
        mock_voice_instance.process_voice_claim.return_value = {
            'transcript': 'I had an accident',
            'confidence': 0.95,
            'keywords': ['accident'],
            'sentiment_score': 0.2,
            'sentiment_label': 'neutral',
            'emotion_scores': {},
            'recording_quality': 'good',
            'word_count': 3,
            'speaking_rate': 120,
            'duration': 10
        }

        mock_soro_instance = mock_soro_service.return_value
        mock_soro_instance.calculate_claim_score.return_value = {
            'soro_score': 45.5,
            'risk_level': 'medium',
            'auto_approval_recommended': False,
            'components': {
                'inconsistency': 30,
                'urgency': 40,
                'sentiment': 50,
                'media_integrity': 70,
                'historical': 60,
                'weighted_inconsistency': 3,
                'weighted_urgency': 4,
                'weighted_sentiment': 5,
                'weighted_media': 7,
                'weighted_historical': 6
            }
        }

        # Create a claim with an audio file
        audio_file = SimpleUploadedFile("test.wav", b"fake audio", content_type="audio/wav")
        claim = create_claim(self.user, self.policy, audio_file=audio_file)
        url = reverse('claim-submit-voice-claim', args=[claim.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('underwriting_result', response.data)

        claim.refresh_from_db()
        self.assertIsNotNone(claim.soro_score)

    def test_review_claim_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('claim-review', args=[self.claim.id])
        data = {'action': 'approve', 'notes': 'Looks good', 'approved_amount': 40000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.claim.refresh_from_db()
        self.assertEqual(self.claim.status, Claim.ClaimStatus.APPROVED)
        self.assertEqual(self.claim.approved_amount, 40000)

    def test_review_claim_as_customer_forbidden(self):
        url = reverse('claim-review', args=[self.claim.id])
        data = {'action': 'approve'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PaymentViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.product = create_product()
        self.policy = create_policy(self.user, self.product)
        self.client.force_authenticate(user=self.user)

    @patch('api.views.PaymentService')
    def test_initiate_payment(self, mock_payment_service):
        mock_instance = mock_payment_service.return_value
        mock_instance.initiate_payment.return_value = {
            'success': True,
            'payment_reference': 'PAY-123456',
            'authorization_url': 'http://test.com/pay'
        }

        url = reverse('payment-initiate-payment')
        data = {
            'amount': 10000,
            'payment_type': 'premium',
            'currency': 'NGN',
            'policy_id': self.policy.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    @patch('api.views.PaymentService')
    def test_verify_payment(self, mock_payment_service):
        mock_instance = mock_payment_service.return_value
        mock_instance.verify_payment.return_value = {
            'success': True,
            'status': 'completed'
        }

        url = reverse('payment-verify-payment')
        data = {'reference': 'PAY-123456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])


class AdminDashboardViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = create_user(phone_number='+2348022222222', user_type='admin')
        self.customer = create_user(phone_number='+2348033333333')
        self.product = create_product()
        self.policy = create_policy(self.customer, self.product)
        self.claim = create_claim(self.customer, self.policy)
        self.url = reverse('admin-dashboard')

    def test_admin_can_access(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('claims_overview', response.data)

    def test_customer_cannot_access(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class USSDViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('ussd')

    @patch('api.views.USSDService')
    def test_ussd_request(self, mock_ussd_service):
        mock_instance = mock_ussd_service.return_value
        expected_response = "CON Welcome to Sorosurance\n" \
                            "1. Buy Insurance\n" \
                            "2. File Claim\n" \
                            "3. Check Policy\n" \
                            "4. Make Payment\n" \
                            "5. Speak to Agent\n"
        mock_instance.process_request.return_value = expected_response

        data = {
            'session_id': '12345',
            'phone_number': '+2348000000000',
            'service_code': '*384*7676#',
            'text': '0' # Changed from '' to '0' to reflect common USSD initial input
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)


class VoiceNotificationViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('voice-notifications')

    @patch('api.views.NotificationService')
    def test_send_voice_notification(self, mock_notification_service):
        mock_instance = mock_notification_service.return_value
        mock_instance.send_voice_notification.return_value = {'success': True}

        data = {
            'type': 'claim_update',
            'message': 'Your claim is approved'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])


# ----------------------------------------------------------------------
# Service Tests (Unit tests with mocking)
# ----------------------------------------------------------------------
class SoroScoreServiceTests(TestCase):
    def setUp(self):
        self.service = SoroScoreService()
        self.user = create_user()
        self.product = create_product()
        self.policy = create_policy(self.user, self.product)
        self.claim = create_claim(self.user, self.policy)

    @patch('random.uniform')
    def test_calculate_claim_score(self, mock_uniform):
        mock_uniform.side_effect = [40.0, 20, 30, 10, 50, 60, 0.8]
        result = self.service.calculate_claim_score(self.claim)
        self.assertIn('soro_score', result)
        self.assertIn('risk_level', result)
        self.assertIn('auto_approval_recommended', result)
        self.assertIn('components', result)

    def test_calculate_user_score(self):
        score = self.service.calculate_user_score(self.user)
        self.assertTrue(30 <= score <= 80)

    def test_calculate_policy_score(self):
        score = self.service.calculate_policy_score(self.policy)
        self.assertTrue(25 <= score <= 75)


class VoiceProcessingServiceTests(TestCase):
    def setUp(self):
        self.service = VoiceProcessingService()

    @patch('api.services.voice_processing_service.AudioSegment.from_file')
    def test_process_voice_claim(self, mock_from_file):
        # Create a dummy audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(b'RIFF....fakewavdata')
            temp_path = f.name

        # Mock AudioSegment
        mock_audio = MagicMock()
        mock_audio.__len__.return_value = 10000  # 10 seconds in ms
        mock_audio.dBFS = -15
        mock_audio.get_array_of_samples.return_value = [0] * 100
        mock_from_file.return_value = mock_audio

        # Mock _transcribe_audio directly to ensure a successful transcript
        with patch('api.services.voice_processing_service.VoiceProcessingService._transcribe_audio') as mock_transcribe_audio:
            mock_transcribe_audio.return_value = {'text': "I had an accident in Lagos", 'confidence': 0.9, 'engine': 'google'}

            result = self.service.process_voice_claim(temp_path)
            self.assertTrue(result['success'])
            self.assertEqual(result['transcript'], "I had an accident in Lagos")
            self.assertIn('keywords', result)
            self.assertIn('sentiment_score', result)

    def test_extract_keywords(self):
        text = "I had a terrible accident with my car in Lagos yesterday"
        keywords = self.service._extract_keywords(text)
        self.assertIn('accident', keywords)
        self.assertIn('lagos', keywords)

    def test_analyze_sentiment(self):
        result = self.service._analyze_sentiment("I am very happy")
        self.assertEqual(result['label'], 'positive')
        result = self.service._analyze_sentiment("This is terrible")
        self.assertEqual(result['label'], 'negative')


class PaymentServiceTests(TestCase):
    def setUp(self):
        self.service = PaymentService()
        self.user = create_user()
        self.payment = Payment.objects.create(
            user=self.user,
            payment_type='premium',
            amount=10000.00,
            currency='NGN',
            payment_gateway='paystack'
        )

    @patch('requests.post')
    @override_settings(BASE_URL='http://testserver')
    def test_initiate_paystack_payment(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': True,
            'data': {
                'reference': 'PAY-123',
                'authorization_url': 'http://paystack.com/authorize'
            }
        }
        mock_post.return_value = mock_response

        result = self.service._initiate_paystack_payment(self.payment)
        self.assertTrue(result['success'])
        self.assertEqual(result['payment_reference'], self.payment.payment_reference)

    @override_settings(BASE_URL='http://testserver')
    def test_mock_payment_initiation(self):
        result = self.service._mock_payment_initiation(self.payment)
        self.assertTrue(result['success'])
        self.assertIn('authorization_url', result)

    @patch('api.services.PaymentService._verify_paystack_payment')
    def test_verify_payment(self, mock_verify):
        mock_verify.return_value = {'success': True, 'status': 'completed'}
        # Ensure the service uses payment_gateway, not gateway
        self.payment.payment_gateway = 'paystack'
        self.payment.save()
        result = self.service.verify_payment(self.payment.payment_reference)
        self.assertTrue(result['success'])


class NotificationServiceTests(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_send_claim_notification_creates_notification(self):
        result = NotificationService.send_claim_notification(
            user=self.user,
            notification_type='voice',
            title='Test',
            message='Hello'
        )
        self.assertTrue(result['success'])
        notification = Notification.objects.first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.user)

    @patch('api.services.NotificationService._send_voice_notification')
    def test_send_voice_notification(self, mock_voice):
        mock_voice.return_value = {'success': True}
        result = NotificationService.send_voice_notification(
            user=self.user,
            message='Test voice'
        )
        self.assertTrue(result['success'])


class USSDServiceTests(TestCase):
    def setUp(self):
        self.service = USSDService()

    def test_welcome_menu(self):
        response = self.service.process_request('123', '+2348000000000', '*384*7676#', '')
        self.assertTrue(response.startswith('CON'))

    def test_main_menu_selection_buy(self):
        response = self.service.process_request('123', '+2348000000000', '*384*7676#', '1')
        self.assertIn('Select Insurance Type', response)

    def test_voice_claim_initiation(self):
        response = self.service.process_request('123', '+2348000000000', '*384*7676#', '2')
        self.assertTrue(response.startswith('END'))
        self.assertIn('voice call', response)

    def test_error_menu(self):
        response = self.service.process_request('123', '+2348000000000', '*384*7676#', '99')
        self.assertTrue(response.startswith('END'))
        self.assertIn('Invalid selection', response)