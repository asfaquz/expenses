from rest_framework import serializers
from .models import User, UserAccount  # Assuming you have a User model defined in models.py


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'mobile_country_code', 'mobile_number', 'nationality']
        # No need to write create() - ModelSerializer does this automatically!
    
    def update(self, instance, validated_data):
        """
        Explicit update method to handle partial updates correctly
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'status', 'user', 'token_generated', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
       

