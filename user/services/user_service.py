from django.db import transaction
from user.models import User
from user.serializers import UserSerializer, UserAccountSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
import logging

# This module handles user-related operations such as creating, updating, and retrieving user information.
# It also includes JWT token generation for authentication.
# Import necessary modules and classes


logger = logging.getLogger(__name__)

class UserService:
    """
    A service class to handle user-related operations.
    """

    @staticmethod
    def get_all_users():
        """
        Get all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return serializer.data

    @staticmethod
    def get_user(user_id):
        """
        Get user details by user ID.
        """
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return serializer.data

    @staticmethod
    def update_user(user_id, data):
        """
        Update user details by user ID.
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        serializer = UserSerializer(
            instance=user,  # This is critical - pass the existing instance
            data=data,
            partial=True  # Allow partial updates
        )

        if serializer.is_valid():
            serializer.save()  # This will call our custom update() method
            return serializer.data
        return None

    @staticmethod
    def create_user(data):
        """
        Create a new user and generate JWT token.
        """
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token_data = UserService.create_jwt_token(user)
            # Add token to the serializer data
            serializer_data = serializer.data
            serializer_data['token'] = token_data
            print(f"User created successfully: {serializer_data}")
            return serializer_data
        return None
    
    @staticmethod
    def activate_user_account(data):
        print(f"Activating user account with data: {data}")
        user_id = data.get('user_id') or data.get('id')
        if not user_id:
            logger.error("User ID is missing in data: %s", data)
            return None
        # Optionally, check if the user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.error(f"User with id {user_id} does not exist.")
            return None

        status = 'active'
        account_serializer = UserAccountSerializer(
            data={
                'status': status,
                'user': user_id,
                'token_generated': True
            }
        )
        if account_serializer.is_valid():
            account_serializer.save()
            return account_serializer.data
        logger.error(f"Account serializer errors: {account_serializer.errors}")
        return None
    
    @staticmethod
    def create_jwt_token(user):
        """
        Create JWT token for the user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }



















