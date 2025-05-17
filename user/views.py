from django.shortcuts import render
from django.http import HttpResponse
from user.services.user_service import UserService
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



@api_view(['GET'])
def index(request):
    return Response({"message": "Welcome to the Expenses Tracker API!"})


@api_view(['GET'])
def get_all_users(request):
    """
    Get all users.
    """
    users = UserService.get_all_users()
    if not users:
        return Response({"message": "No users found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(users)


@api_view(['GET'])
def get_user(request, user_id):
    """
    Get user details by user ID.
    """
    user = UserService.get_user(user_id)  # Better error handling
    if not user:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(user)

@api_view(['POST'])
def create_user(request):
    """
    Create a new user.
    """
    data = request.data
    user = UserService.create_user(data)
    if not user:
        return Response({"message": "User creation failed."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(user, status=status.HTTP_201_CREATED)   

@api_view(['PATCH'])
def update_user(request, user_id):
    """
    Update user details by user ID.
    """
    try:
        user = UserService.update_user(user_id, request.data)
        if not user:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except UserService.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except UserService.ValidationError as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, user_id):
    """
    Delete a user by user ID.
    """
    if request.method == 'DELETE':
        # Handle user deletion logic here
        pass
    return Response({"message": f"User ID: {user_id} deleted."})

@api_view(['POST'])
def create_user_account(request):
    """
    Create a new user account.
    """
    data = request.data
    user = UserService.create_user_account(data)
    if not user:
        return Response({"message": "User account creation failed."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(user, status=status.HTTP_201_CREATED)
    # return Response({"message": "User account created successfully."}, status=status.HTTP_201_CREATED)





