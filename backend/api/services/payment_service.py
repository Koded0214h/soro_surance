import requests
import json
import uuid
from datetime import datetime, timedelta   # added timedelta
from django.conf import settings
from django.utils import timezone
from ..models import Payment, Policy, Claim

base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')

class PaymentService:
    """Service for handling payments"""

    def __init__(self):
        self.paystack_secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
        self.redpay_api_key = getattr(settings, 'REDPAY_API_KEY', '')

    def initiate_payment(self, user, amount, payment_type, currency='NGN',
                        policy_id=None, claim_id=None, voice_confirmation=None):
        """Initiate a payment"""

        # Generate payment reference
        payment_reference = f"PAY-{uuid.uuid4().hex[:10].upper()}"

        # Create payment record
        payment = Payment.objects.create(
            payment_reference=payment_reference,
            user=user,
            payment_type=payment_type,
            amount=amount,
            currency=currency,
            status=Payment.PaymentStatus.PENDING,
            voice_payment=bool(voice_confirmation)
        )

        # Link to policy or claim
        if policy_id:
            try:
                policy = Policy.objects.get(id=policy_id, user=user)
                payment.policy = policy
                payment.save()
            except Policy.DoesNotExist:
                pass

        if claim_id:
            try:
                claim = Claim.objects.get(id=claim_id, user=user)
                payment.claim = claim
                payment.save()
            except Claim.DoesNotExist:
                pass

        # Store voice confirmation if provided
        if voice_confirmation:
            payment.voice_confirmation_file = voice_confirmation
            payment.save()

        # Determine gateway
        use_paystack = self.paystack_secret_key and self.paystack_secret_key not in ['your_paystack_secret_key_here', '']
        use_redpay = self.redpay_api_key and self.redpay_api_key not in ['your_redpay_api_key_here', '']

        if use_paystack:
            return self._initiate_paystack_payment(payment)
        elif use_redpay:
            return self._initiate_redpay_payment(payment)
        else:
            # Mock payment for development
            return self._mock_payment_initiation(payment)

    def _initiate_paystack_payment(self, payment):
        """Initiate payment with Paystack"""
        try:
            url = "https://api.paystack.co/transaction/initialize"
            headers = {
                "Authorization": f"Bearer {self.paystack_secret_key}",
                "Content-Type": "application/json"
            }

            data = {
                "email": payment.user.email,
                "amount": int(float(payment.amount) * 100),  # Convert to kobo
                "reference": payment.payment_reference,
                "currency": payment.currency,
                "callback_url": f"{base_url}/api/payments/verify/{payment.payment_reference}/",
                "metadata": {
                    "user_id": payment.user.id,
                    "payment_type": payment.payment_type,
                    "policy_id": payment.policy.id if payment.policy else None,
                    "claim_id": payment.claim.id if payment.claim else None
                }
            }

            response = requests.post(url, headers=headers, json=data)
            result = response.json()

            if result.get('status'):
                payment.gateway_reference = result['data']['reference']
                payment.gateway_response = result
                payment.save()
                payment.payment_gateway = 'paystack'
                payment.save()

                return {
                    'success': True,
                    'payment_reference': payment.payment_reference,
                    'gateway_reference': payment.gateway_reference,
                    'authorization_url': result['data']['authorization_url'],
                    'message': 'Payment initialized successfully'
                }
            else:
                payment.status = Payment.PaymentStatus.FAILED
                payment.gateway_response = result
                payment.save()

                return {
                    'success': False,
                    'error': result.get('message', 'Payment initialization failed'),
                    'payment_reference': payment.payment_reference
                }

        except Exception as e:
            payment.status = Payment.PaymentStatus.FAILED
            payment.save()

            return {
                'success': False,
                'error': str(e),
                'payment_reference': payment.payment_reference
            }

    def _initiate_redpay_payment(self, payment):
        """Initiate payment with RedPay (placeholder)"""
        # RedPay integration would go here
        # For now, treat as mock
        payment.payment_gateway = 'redpay'
        payment.save()
        return self._mock_payment_initiation(payment)

    def _mock_payment_initiation(self, payment):
        """Mock payment initiation for development"""
        payment.payment_gateway = 'mock'
        payment.save()
        return {
            'success': True,
            'payment_reference': payment.payment_reference,
            'gateway_reference': f"MOCK-{payment.payment_reference}",
            'authorization_url': f"{base_url}/mock-payment/{payment.payment_reference}/",
            'message': 'Mock payment initialized successfully',
            'note': 'This is a mock payment for development'
        }

    def verify_payment(self, reference):
        """Verify payment status"""
        try:
            payment = Payment.objects.get(payment_reference=reference)

            if payment.payment_gateway == 'paystack':
                return self._verify_paystack_payment(payment)
            elif payment.payment_gateway == 'redpay':
                return self._verify_redpay_payment(payment)
            else:
                return self._verify_mock_payment(payment)

        except Payment.DoesNotExist:
            return {
                'success': False,
                'error': 'Payment not found'
            }

    def _verify_paystack_payment(self, payment):
        """Verify Paystack payment"""
        try:
            url = f"https://api.paystack.co/transaction/verify/{payment.gateway_reference}"
            headers = {
                "Authorization": f"Bearer {self.paystack_secret_key}"
            }

            response = requests.get(url, headers=headers)
            result = response.json()

            if result.get('status'):
                data = result['data']

                if data['status'] == 'success':
                    payment.status = Payment.PaymentStatus.COMPLETED
                    payment.completed_at = timezone.now()
                    payment.gateway_response = result
                    payment.save()

                    # Update related objects
                    self._update_after_payment(payment)

                    return {
                        'success': True,
                        'status': 'completed',
                        'message': 'Payment completed successfully',
                        'payment': {
                            'reference': payment.payment_reference,
                            'amount': payment.amount,
                            'currency': payment.currency,
                            'completed_at': payment.completed_at
                        }
                    }
                else:
                    payment.status = Payment.PaymentStatus.FAILED
                    payment.gateway_response = result
                    payment.save()

                    return {
                        'success': False,
                        'status': 'failed',
                        'message': data.get('gateway_response', 'Payment failed')
                    }
            else:
                return {
                    'success': False,
                    'error': result.get('message', 'Verification failed')
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _verify_redpay_payment(self, payment):
        """Verify RedPay payment (placeholder)"""
        # For now, treat as mock
        return self._verify_mock_payment(payment)

    def _verify_mock_payment(self, payment):
        """Verify mock payment (for development)"""
        # Simulate payment verification
        payment.status = Payment.PaymentStatus.COMPLETED
        payment.completed_at = timezone.now()
        payment.save()

        # Update related objects
        self._update_after_payment(payment)

        return {
            'success': True,
            'status': 'completed',
            'message': 'Mock payment completed successfully',
            'payment': {
                'reference': payment.payment_reference,
                'amount': payment.amount,
                'currency': payment.currency,
                'completed_at': payment.completed_at
            }
        }

    def _update_after_payment(self, payment):
        """Update related objects after successful payment"""
        if payment.payment_type == 'premium' and payment.policy:
            # Activate policy
            policy = payment.policy
            policy.status = Policy.PolicyStatus.ACTIVE
            policy.payment_reference = payment.payment_reference
            policy.save()

            # Update next payment date
            if policy.premium_frequency == 'monthly':
                policy.next_payment_date = timezone.now().date() + timedelta(days=30)
            elif policy.premium_frequency == 'quarterly':
                policy.next_payment_date = timezone.now().date() + timedelta(days=90)
            elif policy.premium_frequency == 'annually':
                policy.next_payment_date = timezone.now().date() + timedelta(days=365)
            policy.save()

        elif payment.payment_type == 'claim' and payment.claim:
            # Mark claim as paid
            claim = payment.claim
            claim.status = Claim.ClaimStatus.PAID
            claim.payment_reference = payment.payment_reference
            claim.paid_at = timezone.now()
            claim.save()

            # Update user stats
            user = claim.user
            user.approved_claims += 1
            user.total_claims += 1
            user.save()