from rest_framework import serializers

from profiles_api import models 

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIViews"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email', 'name','password') 
        extra_kwargs = {
            'password': {
                'write_only':True, 
                # won't see input when typing password
                'style': {'input_type':'password'}
            }
        }

    # password created as hash
    def create(self, validated_data):
        """Create and return a new user. Overwrite the create funcation to hash the password.
        By default django would call model.objects.create() instead of 
        model.xxx.objects.create_user()
        """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
          
        )

        return user 

    def update(self, instance, validated_data):
        """Handle updating user account.
        Password requires additional logic to hash the password before saving the update"""
        if 'password' in validated_data:
            #assign value and remove from dictionary
            password = validated_data.pop('password')
            #saves as a hash
            instance.set_password(password)
        
        # pass the values to the existing DRF update() method
        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }