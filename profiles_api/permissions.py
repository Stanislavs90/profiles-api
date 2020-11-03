from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile. 
        Functions are passed 
        """
        # if request is in safe methods such as get
        if request.method in permissions.SAFE_METHODS: 
            return True 

        # auth id == request user id 
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            # if true allows request
            return True

        # status assigned to the user making the request
        return obj.user_profile.id == request.user.id 