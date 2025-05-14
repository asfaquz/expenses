from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework import status


@api_view(['GET'])
def index(request):
    return Response({"message": "Welcome to the Expenses Tracker API!"})


@api_view(['GET'])
def get_all_users(request):
    """
    Get all users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user(request, user_id):
    """
    Get user details by user ID.
    """
    user = get_object_or_404(User, id=user_id)  # Better error handling
    serializer = UserSerializer(user) 
    return Response(serializer.data)


@api_view(['PATCH'])
def update_user(request, user_id):
    """
    Update user details by user ID.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(
        instance=user,  # This is critical - pass the existing instance
        data=request.data,
        partial=True  # Allow partial updates
    )
    
    if serializer.is_valid():
        serializer.save()  # This will call our custom update() method
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_user(request):
    """
    Create a new user.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Save the user to the database
        serializer.save()
        return Response({"message": "User created successfully.", "data": serializer.validated_data})
    else:
        return Response({"errors": serializer.errors}, status=400)
    # Handle user creation logic here
        

@api_view(['DELETE'])
def delete_user(request, user_id):
    """
    Delete a user by user ID.
    """
    if request.method == 'DELETE':
        # Handle user deletion logic here
        pass
    return Response({"message": f"User ID: {user_id} deleted."})


