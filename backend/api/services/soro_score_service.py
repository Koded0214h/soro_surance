from django.conf import settings
import random

class SoroScoreService:
    """
    Service for calculating Soro-Scores for users, policies, and claims.
    This is a mock implementation for demonstration purposes.
    """

    def calculate_claim_score(self, claim):
        """
        Calculates a Soro-Score for a given claim.
        In a real scenario, this would involve complex AI/ML models.
        """
        # Mocking some logic for demonstration
        soro_score = random.uniform(20.0, 90.0)
        risk_level = 'low'
        auto_approval_recommended = False

        if soro_score > 70:
            risk_level = 'high'
            auto_approval_recommended = False
        elif soro_score > 40:
            risk_level = 'medium'
            # Simulate auto-approval for some medium-risk claims
            if random.random() > 0.7:
                auto_approval_recommended = True
        else:
            risk_level = 'low'
            auto_approval_recommended = True
        
        # Mock components based on weights from settings
        weights = settings.SORO_SCORE_WEIGHTS
        inconsistency = random.uniform(0, 100)
        urgency = random.uniform(0, 100)
        sentiment = random.uniform(0, 100)
        media_integrity = random.uniform(0, 100)
        historical = random.uniform(0, 100)

        return {
            'soro_score': soro_score,
            'risk_level': risk_level,
            'auto_approval_recommended': auto_approval_recommended,
            'confidence': random.uniform(0.6, 0.99),
            'components': {
                'inconsistency': inconsistency,
                'urgency': urgency,
                'sentiment': sentiment,
                'media_integrity': media_integrity,
                'historical': historical,
                'weighted_inconsistency': inconsistency * weights.get('inconsistency', 0),
                'weighted_urgency': urgency * weights.get('urgency', 0),
                'weighted_sentiment': sentiment * weights.get('sentiment', 0),
                'weighted_media': media_integrity * weights.get('media_integrity', 0),
                'weighted_historical': historical * weights.get('historical', 0),
            },
            'flags': ['mock_flag_1', 'mock_flag_2'] if soro_score > 70 else [],
            'recommendation': 'Approve' if auto_approval_recommended else 'Review Manually'
        }

    def calculate_user_score(self, user):
        """Calculates a Soro-Score for a given user."""
        # This would be a more complex calculation based on user history, demographics, etc.
        return random.uniform(30.0, 80.0)

    def calculate_policy_score(self, policy):
        """Calculates a Soro-Score for a given policy."""
        # This would factor in product type, user score, coverage details, etc.
        return random.uniform(25.0, 75.0)

