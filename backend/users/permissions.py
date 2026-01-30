from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Object-level permission to only allow owners or admins to access"""
    
    def has_object_permission(self, request, view, obj):
        # Check if user is admin or reviewer
        if request.user.user_type in ['admin', 'reviewer']:
            return True
        
        # Check if user owns the object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsAdminOrReviewer(permissions.BasePermission):
    """Permission to only allow admin or reviewer users"""
    
    def has_permission(self, request, view):
        return request.user.user_type in ['admin', 'reviewer']
    
    def has_object_permission(self, request, view, obj):
        return request.user.user_type in ['admin', 'reviewer']


class IsCustomer(permissions.BasePermission):
    """Permission to only allow customer users"""
    
    def has_permission(self, request, view):
        return request.user.user_type == 'customer'
    
    def has_object_permission(self, request, view, obj):
        return request.user.user_type == 'customer'


class IsAgent(permissions.BasePermission):
    """Permission to only allow agent users"""
    
    def has_permission(self, request, view):
        return request.user.user_type == 'agent'
    
    def has_object_permission(self, request, view, obj):
        return request.user.user_type == 'agent'