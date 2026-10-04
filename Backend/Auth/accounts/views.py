from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User

# Signup
@api_view(['POST'])
def signup(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(email=email).exists():
        return Response({"msg": "Email already exists"})

    User.objects.create(
        name=name,
        email=email,
        password=password
    )

    return Response({"msg": "Signup Success"})


# Login
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email, password=password).first()

    if user:
        return Response({"msg": "Login Success", "name": user.name})
    else:
        return Response({"msg": "Invalid Credentials"})
    

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