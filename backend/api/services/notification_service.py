import requests
import json
from django.conf import settings
from django.utils import timezone
from ..models import Notification
import uuid


class NotificationService:
    """Service for sending notifications"""
    
    @staticmethod
    def send_claim_notification(user, notification_type, title, message, claim=None, policy=None):
        """Send claim-related notification"""
        
        # Create notification record
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            claim=claim,
            policy=policy,
            status=Notification.NotificationStatus.PENDING
        )
        
        # Send based on notification type
        if notification_type == 'voice':
            return NotificationService._send_voice_notification(notification)
        elif notification_type == 'whatsapp':
            return NotificationService._send_whatsapp_notification(notification)
        elif notification_type == 'sms':
            return NotificationService._send_sms_notification(notification)
        elif notification_type == 'email':
            return NotificationService._send_email_notification(notification)
        else:
            # Default to updating status
            notification.status = Notification.NotificationStatus.SENT
            notification.sent_at = timezone.now()
            notification.save()
            return {'success': True, 'notification_id': notification.id}
    
    @staticmethod
    def _send_voice_notification(notification):
        """Send voice notification"""
        try:
            # For hackathon: Simulate voice notification
            # In production, integrate with Africa's Talking or similar service
            
            notification.voice_message = notification.message
            notification.status = Notification.NotificationStatus.SENT
            notification.sent_at = timezone.now()
            notification.save()
            
            # Simulate delivery
            notification.status = Notification.NotificationStatus.DELIVERED
            notification.delivered_at = timezone.now()
            notification.save()
            
            return {
                'success': True,
                'notification_id': notification.id,
                'type': 'voice',
                'message': 'Voice notification queued for delivery'
            }
            
        except Exception as e:
            notification.status = Notification.NotificationStatus.FAILED
            notification.save()
            
            return {
                'success': False,
                'error': str(e),
                'notification_id': notification.id
            }
    
    @staticmethod
    def _send_whatsapp_notification(notification):
        """Send WhatsApp notification"""
        try:
            # Integrate with WhatsApp Business API or Africa's Talking
            whatsapp_number = notification.user.whatsapp_number or notification.user.phone_number
            
            # For hackathon: Simulate WhatsApp notification
            notification.status = Notification.NotificationStatus.SENT
            notification.sent_at = timezone.now()
            notification.save()
            
            # Simulate delivery
            notification.status = Notification.NotificationStatus.DELIVERED
            notification.delivered_at = timezone.now()
            notification.save()
            
            return {
                'success': True,
                'notification_id': notification.id,
                'type': 'whatsapp',
                'recipient': whatsapp_number,
                'message': 'WhatsApp notification sent'
            }
            
        except Exception as e:
            notification.status = Notification.NotificationStatus.FAILED
            notification.save()
            
            return {
                'success': False,
                'error': str(e),
                'notification_id': notification.id
            }
    
    @staticmethod
    def send_voice_notification(user, message, notification_type='claim_update', claim=None, policy=None):
        """Send a voice notification to user"""
        return NotificationService.send_claim_notification(
            user=user,
            notification_type='voice',
            title=f"{notification_type.replace('_', ' ').title()}",
            message=message,
            claim=claim,
            policy=policy
        )