from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.decorator.permission import *
from user.models import User
from user.func import generate_token, hash_password


@csrf_exempt
@superadmin_required
def register_admin(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
    except:
        return JsonResponse({"message": "Missing fields"}, status=400)

    try:
        user = User.objects.get(username=username)
        return JsonResponse({"message": "Username already exists"}, status=400)
    except:
        pass

    try:
        user = User.objects.get(email=email)
        return JsonResponse({"message": "Email already exists"}, status=400)
    except:
        pass

    password = hash_password(password)
    User.objects.create(username=username, password=password, email=email, is_admin=True)

    return JsonResponse({"message": "Admin created successfully"}, status=201)


@csrf_exempt
@admin_required
def register_staff(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
    except:
        return JsonResponse({"message": "Missing fields"}, status=400)

    try:
        user = User.objects.get(username=username)
        return JsonResponse({"message": "Username already exists"}, status=400)
    except:
        pass

    try:
        user = User.objects.get(email=email)
        return JsonResponse({"message": "Email already exists"}, status=400)
    except:
        pass

    password = hash_password(password)
    User.objects.create(username=username, password=password, email=email, is_staff=True)

    return JsonResponse({"message": "Staff created successfully"}, status=201)


@csrf_exempt
def register_customer(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        name = request.POST.get('name', None)
    except:
        return JsonResponse({"message": "Missing fields"}, status=400)

    try:
        user = User.objects.get(username=username)
        return JsonResponse({"message": "Username already exists"}, status=400)
    except:
        pass

    try:
        user = User.objects.get(email=email)
        return JsonResponse({"message": "Email already exists"}, status=400)
    except:
        pass

    password = hash_password(password)
    user = User.objects.create(
        username=username,
        password=password,
        email=email,
        name=name,
    )
    token = generate_token(user.id)

    return JsonResponse({
        "success": True,
        "message": "Customer created successfully",
        "token": token
    }, status=201)


@csrf_exempt
def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return JsonResponse({"message": "Missing fields"}, status=400)

    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({"message": "User not found"}, status=404)

    if user.password != hash_password(password):
        return JsonResponse({"message": "Incorrect password"}, status=400)

    token = generate_token(user.id)

    return JsonResponse({
        "success": True,
        "message": "Login successful",
        "token": token
    }, status=200)