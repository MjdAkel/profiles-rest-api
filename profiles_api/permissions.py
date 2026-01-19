from rest_framework import permissions
# Custom permission to allow users to edit their own profile
class UpdateOwnProfile(permissions.BasePermission):
    """allow users to edit their own profile"""
    def has_object_permission(self, request, view, obj):
        """check that user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS: #SAFE_METHODS are GET, HEAD, OPTIONS 
            return True #allow read-only access for safe methods
        
        return obj.id == request.user.id #check if the object being accessed belongs to the authenticated user if no SAFE_METHODS if yes return true else false 
    
class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status feed items"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id   