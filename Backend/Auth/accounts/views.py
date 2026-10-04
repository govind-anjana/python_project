from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User

# Signup
@api_view(['POST'])
def signup(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all(isinstance(value, str) for value in (name, email, password)):
        return Response(
            {"msg": "Name, email, and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    name = name.strip()
    email = email.strip().lower()
    if not name or len(name) > 100:
        return Response(
            {"msg": "Enter a name between 1 and 100 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        validate_email(email)
        validate_password(password)
    except ValidationError as error:
        return Response(
            {"msg": error.messages[0]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email__iexact=email).exists():
        return Response(
            {"msg": "Email already exists"},
            status=status.HTTP_409_CONFLICT,
        )

    User.objects.create(
        name=name,
        email=email,
        password=make_password(password),
    )

    return Response(
        {"msg": "Signup Success"},
        status=status.HTTP_201_CREATED,
    )


# Login
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not isinstance(email, str) or not isinstance(password, str):
        return Response(
            {"msg": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.filter(email__iexact=email.strip()).first()

    if user and check_password(password, user.password):
        return Response({"msg": "Login Success", "name": user.name})

    if user and user.password == password:
        user.password = make_password(password)
        user.save(update_fields=["password"])
        return Response({"msg": "Login Success", "name": user.name})

    return Response(
        {"msg": "Invalid Credentials"},
        status=status.HTTP_401_UNAUTHORIZED,
    )

# GET All Users
@api_view(['GET'])
def get_users(request):
    users = User.objects.all()

    data = []

    for u in users:
        data.append({
            "id": u.id,
            "name": u.name,
            "email": u.email
        })

    return Response(data)

@api_view(['GET'])
def single_user(request, id):
    user = User.objects.get(id=id)

    data = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

    return Response(data)