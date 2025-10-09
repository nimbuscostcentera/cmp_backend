from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from masters.models import UserMaster
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password


@api_view(['POST'])
def registeruser(request):
    print("in register")
    # Map frontend keys to model fields
    contact = request.data.get('Contact')  # match case
    password = request.data.get('Password')
    User_Name = request.data.get('User_Name')
    UType = request.data.get('UType')
    active = request.data.get('active', True)

    # Validation
    if not contact or not password or not User_Name:
        return Response({"error": "All fields are required"}, status=400)

    if UserMaster.objects.filter(Contact=contact).exists():
        return Response({"error": "User already exists"}, status=403)

    hashed_password = make_password(password)

    user = UserMaster.objects.create(
        Contact=contact,
        Password=hashed_password,
        User_Name=User_Name,
        UType=UType,
        active=active,
    )

    return Response({"success": "User registered successfully", "user_id": user.User_ID}, status=201)



@api_view(['POST'])  # Only POST for login is standard
def getlogin(request):
    contact = request.data.get('contact')
    password = request.data.get('password')

    if not contact or not password:
        return Response({"error": "Contact and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserMaster.objects.get(Contact=contact)
    except UserMaster.DoesNotExist:
        return Response({"error": "Contact not registered"}, status=status.HTTP_404_NOT_FOUND)

    if not user.active:
        return Response({"error": "User is not active"}, status=status.HTTP_403_FORBIDDEN)

    # Check the hashed password
    if not check_password(password, user.Password):
        return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)
    user.id = user.User_ID 
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Prepare user data to send in response
    user_data = {
        "User_ID": user.User_ID,
        "User_Name": user.User_Name,
        "Contact": user.Contact,
        "UType": user.UType,
        "active": user.active,
    }

    return Response({
        "message": "Login successful",
        "access": access_token,
        "refresh": refresh_token,
        "user": user_data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def edituser(request):
    # print("in edituser")
    user_id = request.data.get('User_ID')
    contact = request.data.get('contact')
    password = request.data.get('password')
    User_Name = request.data.get('User_Name')
    UType = request.data.get('UType')
    active = request.data.get('active', True)  # default True if not provided

    if not user_id:
        return Response({"error": "User_ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the user by ID
    try:
        user = UserMaster.objects.get(User_ID=user_id)
    except UserMaster.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update fields if provided
    if contact:
        user.Contact = contact
    if password:
        user.Password = make_password(password)
    if User_Name:
        user.User_Name = User_Name
    if UType:
        user.UType = UType
    user.active = active

    user.save()

    return Response(
        {"success": "User updated successfully", "user": user.Contact},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def deleteuser(request):
    
    user_id = request.data.get('User_ID')


    if not user_id:
        return Response({"error": "User_ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the user by ID
    try:
        user = UserMaster.objects.get(User_ID=user_id)
    except UserMaster.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



    user.delete()

    return Response(
        {"success": "User deleted successfully", "user_id": user.Contact},
        status=status.HTTP_200_OK
    )
@api_view(["POST"])
def showuser(request):
    # Collect filters from request
    filters = {}
    user_id = request.data.get('User_ID') or request.query_params.get('User_ID')
    contact = request.data.get('contact') or request.query_params.get('contact')
    utype = request.data.get('UType') or request.query_params.get('UType')
    active = request.data.get('active') or request.query_params.get('active')

    if user_id:
        filters['User_ID'] = user_id
    if contact:
        filters['Contact__icontains'] = contact   # case-insensitive search
    if utype:
        filters['UType'] = utype
    if active is not None:
        filters['active'] = active in ["true", "True", True, 1, "1"]

    # Fetch filtered users
    users = UserMaster.objects.filter(**filters).values(
        "User_ID", "Contact", "User_Name", "UType", "active"
    )

    if not users:
        return Response({"message": "No users found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(list(users), status=status.HTTP_200_OK)