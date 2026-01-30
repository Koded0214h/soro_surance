from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.InsuranceProductViewSet, basename='product')
router.register(r'policies', views.PolicyViewSet, basename='policy')
router.register(r'claims', views.ClaimViewSet, basename='claim')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    
    # Admin dashboard
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    
    # USSD endpoint
    path('ussd/', views.USSDView.as_view(), name='ussd'),
    
    # Voice notifications
    path('notifications/voice/', views.VoiceNotificationView.as_view(), name='voice-notifications'),
    
    # Payment endpoints
    path('payments/initiate/', views.PaymentViewSet.as_view({'post': 'initiate_payment'}), name='initiate-payment'),
    path('payments/verify/', views.PaymentViewSet.as_view({'post': 'verify_payment'}), name='verify-payment'),
    
    # Claim voice processing
    path('claims/<int:pk>/submit-voice/', views.ClaimViewSet.as_view({'post': 'submit_voice_claim'}), name='submit-voice-claim'),
    path('claims/<int:pk>/review/', views.ClaimViewSet.as_view({'post': 'review'}), name='review-claim'),
]