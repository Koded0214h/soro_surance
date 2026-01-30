from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
import uuid
import json

from .models import (
    InsuranceProduct, Policy, Claim, VoiceAnalysis,
    SoroScoreLog, Payment, Notification, AdminDashboard
)
from .serializers import (
    InsuranceProductSerializer, PolicySerializer, ClaimSerializer,
    VoiceAnalysisSerializer, SoroScoreLogSerializer, PaymentSerializer,
    NotificationSerializer, AdminDashboardSerializer,
    VoiceClaimSerializer, UnderwritingResultSerializer,
    PaymentInitiationSerializer, USSDRequestSerializer
)
from .services import (
    SoroScoreService, VoiceProcessingService,
    PaymentService, NotificationService, USSDService
)
from users.permissions import IsOwnerOrAdmin, IsAdminOrReviewer, IsCustomer


class InsuranceProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for insurance products"""
    queryset = InsuranceProduct.objects.filter(is_active=True)
    serializer_class = InsuranceProductSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=True, methods=['post'])
    def calculate_premium(self, request, pk=None):
        """Calculate premium for a specific product"""
        product = self.get_object()
        
        # Get user Soro-Score from request user or provided data
        user = request.user if request.user.is_authenticated else None
        soro_score = request.data.get('soro_score')
        
        if user and user.is_authenticated:
            soro_score = user.soro_score
        elif not soro_score:
            soro_score = 50.0  # Default score
        
        # Calculate dynamic premium based on Soro-Score
        base_premium = float(product.base_premium)
        risk_factor = soro_score / 100
        
        # Premium adjustment based on risk
        if soro_score <= 30:
            premium_adjustment = -0.2  # 20% discount for low risk
        elif soro_score <= 70:
            premium_adjustment = 0  # No adjustment for medium risk
        else:
            premium_adjustment = 0.3  # 30% increase for high risk
        
        calculated_premium = base_premium * (1 + premium_adjustment)
        
        # Ensure premium is within min/max bounds
        calculated_premium = max(float(product.min_premium), 
                               min(float(product.max_premium), calculated_premium))
        
        return Response({
            'product': product.name,
            'base_premium': base_premium,
            'soro_score': soro_score,
            'risk_level': 'low' if soro_score <= 30 else 'medium' if soro_score <= 70 else 'high',
            'premium_adjustment': premium_adjustment,
            'calculated_premium': calculated_premium,
            'coverage_amount': product.coverage_details.get('max_coverage', 0)
        })


class PolicyViewSet(viewsets.ModelViewSet):
    """ViewSet for insurance policies"""
    serializer_class = PolicySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['admin', 'reviewer']:
            return Policy.objects.all()
        return Policy.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        
        # Calculate initial premium
        soro_score = user.soro_score
        base_premium = float(product.base_premium)
        
        # Premium adjustment based on Soro-Score
        if soro_score <= 30:
            premium_adjustment = -0.2
        elif soro_score <= 70:
            premium_adjustment = 0
        else:
            premium_adjustment = 0.3
        
        premium_amount = base_premium * (1 + premium_adjustment)
        premium_amount = max(float(product.min_premium), 
                           min(float(product.max_premium), premium_amount))
        
        # Generate policy number
        policy_number = f"SORO-{uuid.uuid4().hex[:8].upper()}"
        
        serializer.save(
            user=user,
            policy_number=policy_number,
            initial_soro_score=soro_score,
            current_soro_score=soro_score,
            premium_amount=premium_amount,
            coverage_amount=product.coverage_details.get('max_coverage', 1000000),
            deductible_amount=product.coverage_details.get('deductible', 5000)
        )
    
    @action(detail=True, methods=['get'])
    def claims(self, request, pk=None):
        """Get all claims for a policy"""
        policy = self.get_object()
        claims = policy.claims.all()
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        """Renew a policy"""
        policy = self.get_object()
        
        if policy.status != policy.PolicyStatus.ACTIVE:
            return Response(
                {'error': 'Only active policies can be renewed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate new premium based on updated Soro-Score
        user = policy.user
        product = policy.product
        
        # Recalculate premium with current Soro-Score
        soro_score = user.soro_score
        base_premium = float(product.base_premium)
        
        if soro_score <= 30:
            premium_adjustment = -0.2
        elif soro_score <= 70:
            premium_adjustment = 0
        else:
            premium_adjustment = 0.3
        
        new_premium = base_premium * (1 + premium_adjustment)
        new_premium = max(float(product.min_premium), 
                         min(float(product.max_premium), new_premium))
        
        # Create renewal record
        renewal_data = {
            'user': user,
            'product': product,
            'start_date': timezone.now().date() + timedelta(days=1),
            'end_date': timezone.now().date() + timedelta(days=366),  # 1 year
            'initial_soro_score': soro_score,
            'current_soro_score': soro_score,
            'premium_amount': new_premium,
            'coverage_amount': policy.coverage_amount,
            'deductible_amount': policy.deductible_amount,
            'status': Policy.PolicyStatus.PENDING,
            'coverage_details': policy.coverage_details
        }
        
        new_policy = Policy.objects.create(**renewal_data)
        
        # Update old policy
        policy.status = Policy.PolicyStatus.EXPIRED
        policy.save()
        
        return Response({
            'message': 'Policy renewal initiated',
            'new_policy': PolicySerializer(new_policy).data,
            'payment_required': new_premium
        })


class ClaimViewSet(viewsets.ModelViewSet):
    """ViewSet for insurance claims"""
    serializer_class = ClaimSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['admin', 'reviewer']:
            return Claim.objects.all()
        return Claim.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        policy = serializer.validated_data['policy']
        
        # Verify user owns the policy
        if policy.user != user:
            raise PermissionError("You don't have permission to file a claim for this policy")
        
        # Generate claim number
        claim_number = f"CLM-{uuid.uuid4().hex[:8].upper()}"
        
        serializer.save(
            user=user,
            claim_number=claim_number,
            status=Claim.ClaimStatus.SUBMITTED,
            submitted_at=timezone.now()
        )
    
    @action(detail=True, methods=['post'])
    def submit_voice_claim(self, request, pk=None):
        """Submit a voice claim"""
        claim = self.get_object()
        
        if claim.audio_file:
            # Process voice claim
            voice_service = VoiceProcessingService()
            analysis_result = voice_service.process_voice_claim(claim.audio_file.path)
            
            # Update claim with voice analysis
            claim.transcript = analysis_result.get('transcript')
            claim.transcript_confidence = analysis_result.get('confidence')
            claim.keywords = analysis_result.get('keywords', [])
            claim.sentiment_score = analysis_result.get('sentiment_score')
            
            # Calculate Soro-Score
            soro_service = SoroScoreService()
            underwriting_result = soro_service.calculate_claim_score(claim)
            
            claim.soro_score = underwriting_result['soro_score']
            claim.risk_level = underwriting_result['risk_level']
            claim.auto_approval_recommended = underwriting_result['auto_approval_recommended']
            claim.inconsistency_score = underwriting_result['components']['inconsistency']
            claim.urgency_score = underwriting_result['components']['urgency']
            
            claim.save()
            
            # Create voice analysis record
            VoiceAnalysis.objects.create(
                claim=claim,
                word_count=analysis_result.get('word_count'),
                speaking_rate=analysis_result.get('speaking_rate'),
                sentiment_label=analysis_result.get('sentiment_label'),
                sentiment_scores=analysis_result.get('sentiment_scores', {}),
                emotion_scores=analysis_result.get('emotion_scores', {}),
                recording_quality=analysis_result.get('recording_quality'),
                confidence_score=analysis_result.get('confidence')
            )
            
            # Log Soro-Score calculation
            SoroScoreLog.objects.create(
                claim=claim,
                user=claim.user,
                inconsistency_score=underwriting_result['components']['inconsistency'],
                urgency_score=underwriting_result['components']['urgency'],
                sentiment_score=underwriting_result['components']['sentiment'],
                media_integrity_score=underwriting_result['components']['media_integrity'],
                historical_score=underwriting_result['components']['historical'],
                weighted_inconsistency=underwriting_result['components']['weighted_inconsistency'],
                weighted_urgency=underwriting_result['components']['weighted_urgency'],
                weighted_sentiment=underwriting_result['components']['weighted_sentiment'],
                weighted_media=underwriting_result['components']['weighted_media'],
                weighted_historical=underwriting_result['components']['weighted_historical'],
                final_soro_score=underwriting_result['soro_score'],
                risk_level=underwriting_result['risk_level'],
                calculation_metadata=underwriting_result
            )
            
            # Send notification
            if claim.auto_approval_recommended:
                claim.status = Claim.ClaimStatus.APPROVED
                claim.save()
                
                NotificationService.send_claim_notification(
                    claim.user,
                    'voice',
                    'Claim Auto-Approved',
                    f'Your claim {claim.claim_number} has been automatically approved.',
                    claim=claim
                )
            
            return Response({
                'message': 'Voice claim processed successfully',
                'claim': ClaimSerializer(claim).data,
                'underwriting_result': underwriting_result
            })
        
        return Response(
            {'error': 'No audio file found for voice claim'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Review a claim (admin/reviewer only)"""
        if not request.user.user_type in ['admin', 'reviewer']:
            return Response(
                {'error': 'Only admins and reviewers can review claims'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        claim = self.get_object()
        action_type = request.data.get('action')  # approve, reject, request_info
        notes = request.data.get('notes', '')
        
        if action_type == 'approve':
            claim.status = Claim.ClaimStatus.APPROVED
            claim.approved_amount = request.data.get('approved_amount', claim.claimed_amount)
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            claim.review_notes = notes
            claim.save()
            
            # Send notification
            NotificationService.send_claim_notification(
                claim.user,
                'voice' if claim.user.prefers_voice else 'whatsapp',
                'Claim Approved',
                f'Your claim {claim.claim_number} has been approved for ₦{claim.approved_amount}.',
                claim=claim
            )
            
        elif action_type == 'reject':
            claim.status = Claim.ClaimStatus.REJECTED
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            claim.review_notes = notes
            claim.save()
            
            # Update user stats
            claim.user.rejected_claims += 1
            claim.user.total_claims += 1
            claim.user.save()
            
            # Send notification
            NotificationService.send_claim_notification(
                claim.user,
                'voice' if claim.user.prefers_voice else 'whatsapp',
                'Claim Rejected',
                f'Your claim {claim.claim_number} has been rejected. Reason: {notes}',
                claim=claim
            )
        
        return Response({
            'message': f'Claim {action_type}ed successfully',
            'claim': ClaimSerializer(claim).data
        })


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for payments"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['admin', 'reviewer']:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)
    
    @action(detail=False, methods=['post'])
    def initiate_payment(self, request):
        """Initiate a payment"""
        serializer = PaymentInitiationSerializer(data=request.data)
        if serializer.is_valid():
            payment_service = PaymentService()
            payment_result = payment_service.initiate_payment(
                user=request.user,
                amount=serializer.validated_data['amount'],
                payment_type=serializer.validated_data['payment_type'],
                currency=serializer.validated_data.get('currency', 'NGN'),
                policy_id=serializer.validated_data.get('policy_id'),
                claim_id=serializer.validated_data.get('claim_id'),
                voice_confirmation=serializer.validated_data.get('voice_confirmation')
            )
            
            return Response(payment_result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_payment(self, request):
        """Verify a payment"""
        reference = request.data.get('reference')
        if not reference:
            return Response(
                {'error': 'Payment reference is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment_service = PaymentService()
        verification_result = payment_service.verify_payment(reference)
        
        return Response(verification_result)


class AdminDashboardView(APIView):
    """Admin dashboard view"""
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReviewer]
    
    def get(self, request):
        # Get risk heatmap data
        claims_by_risk = Claim.objects.values('risk_level').annotate(
            count=Count('id'),
            avg_amount=Avg('claimed_amount'),
            approval_rate=Avg(
                Case(
                    When(status=Claim.ClaimStatus.APPROVED, then=1),
                    When(status=Claim.ClaimStatus.REJECTED, then=0),
                    default=0,
                    output_field=models.FloatField()
                )
            )
        )
        
        # Get claims overview
        total_claims = Claim.objects.count()
        pending_claims = Claim.objects.filter(status=Claim.ClaimStatus.UNDER_REVIEW).count()
        approved_claims = Claim.objects.filter(status=Claim.ClaimStatus.APPROVED).count()
        paid_claims = Claim.objects.filter(status=Claim.ClaimStatus.PAID).count()
        
        # Get revenue data
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        weekly_revenue = Payment.objects.filter(
            status=Payment.PaymentStatus.COMPLETED,
            initiated_at__date__gte=week_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_revenue = Payment.objects.filter(
            status=Payment.PaymentStatus.COMPLETED,
            initiated_at__date__gte=month_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get user analytics
        total_users = User.objects.count()
        new_users_week = User.objects.filter(date_joined__date__gte=week_ago).count()
        active_policies = Policy.objects.filter(status=Policy.PolicyStatus.ACTIVE).count()
        
        dashboard_data = {
            'risk_heatmap': list(claims_by_risk),
            'claims_overview': {
                'total': total_claims,
                'pending': pending_claims,
                'approved': approved_claims,
                'paid': paid_claims,
                'rejection_rate': (Claim.objects.filter(status=Claim.ClaimStatus.REJECTED).count() / total_claims * 100) if total_claims > 0 else 0
            },
            'revenue': {
                'weekly': float(weekly_revenue),
                'monthly': float(monthly_revenue),
                'currency': 'NGN'
            },
            'user_analytics': {
                'total_users': total_users,
                'new_users_week': new_users_week,
                'active_policies': active_policies,
                'customer_growth': (new_users_week / total_users * 100) if total_users > 0 else 0
            },
            'voice_claims_stats': {
                'total_voice_claims': Claim.objects.exclude(audio_file='').count(),
                'auto_approval_rate': (Claim.objects.filter(auto_approval_recommended=True).count() / total_claims * 100) if total_claims > 0 else 0,
                'avg_processing_time': '2.5 hours'  # This would be calculated from actual data
            }
        }
        
        # Update dashboard cache
        dashboard, created = AdminDashboard.objects.get_or_create(
            dashboard_type=AdminDashboard.DashboardType.CLAIMS_OVERVIEW
        )
        dashboard.data = dashboard_data
        dashboard.save()
        
        return Response(dashboard_data)


class USSDView(APIView):
    """Handle USSD requests"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = USSDRequestSerializer(data=request.data)
        if serializer.is_valid():
            ussd_service = USSDService()
            response = ussd_service.process_request(
                session_id=serializer.validated_data['session_id'],
                phone_number=serializer.validated_data['phone_number'],
                service_code=serializer.validated_data['service_code'],
                text=serializer.validated_data['text']
            )
            
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoiceNotificationView(APIView):
    """Handle voice notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        notification_type = request.data.get('type')
        message = request.data.get('message')
        claim_id = request.data.get('claim_id')
        policy_id = request.data.get('policy_id')
        
        if not notification_type or not message:
            return Response(
                {'error': 'Type and message are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        claim = None
        if claim_id:
            try:
                claim = Claim.objects.get(id=claim_id, user=request.user)
            except Claim.DoesNotExist:
                return Response(
                    {'error': 'Claim not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        policy = None
        if policy_id:
            try:
                policy = Policy.objects.get(id=policy_id, user=request.user)
            except Policy.DoesNotExist:
                return Response(
                    {'error': 'Policy not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Send voice notification
        notification_service = NotificationService()
        result = notification_service.send_voice_notification(
            user=request.user,
            message=message,
            notification_type=notification_type,
            claim=claim,
            policy=policy
        )
        
        return Response(result)