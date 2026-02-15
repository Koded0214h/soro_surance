from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from .models import User, UserProfile, UserActivity
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserSerializer, UserProfileSerializer,
    UserActivitySerializer, PasswordChangeSerializer
)
from .permissions import IsOwnerOrAdmin, IsAdminOrReviewer


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # User profile is created automatically via signal
            # UserProfile.objects.create(user=user)
            
            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='registration',
                description='User registered on platform'
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='login',
                description='User logged into platform'
            )
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Log activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='logout',
                description='User logged out of platform'
            )
            
            logout(request)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['admin', 'reviewer']:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='profile_update',
                description='User updated profile information'
            )
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='password_change',
                description='User changed password'
            )
            
            return Response({'message': 'Password updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        user = self.get_object()
        activities = user.activities.all()
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['admin', 'reviewer']:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        # Log activity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='profile_creation',
            description='User created extended profile'
        )
    
    def perform_update(self, serializer):
        serializer.save()
        
        # Log activity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='profile_update',
            description='User updated extended profile'
        )


class AdminUserViewSet(viewsets.ModelViewSet):
    """Admin-only user management"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReviewer]
    queryset = User.objects.all()

    @action(detail=True, methods=['post'])
    def update_soro_score(self, request, pk=None):
        user = self.get_object()
        new_score = request.data.get('soro_score')
        
        if new_score is None:
            return Response(
                {'error': 'soro_score is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_score = float(new_score)
            if not 0 <= new_score <= 100:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'soro_score must be a number between 0 and 100'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_score = user.soro_score
        user.soro_score = new_score
        user.save()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='soro_score_update',
            description=f'Admin updated Soro-Score from {old_score} to {new_score}',
            metadata={
                'target_user': user.id,
                'old_score': old_score,
                'new_score': new_score
            }
        )
        
        return Response({
            'message': f'Soro-Score updated from {old_score} to {new_score}',
            'user': UserSerializer(user).data
        })