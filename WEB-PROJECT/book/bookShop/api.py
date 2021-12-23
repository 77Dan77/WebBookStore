import json
from django.http import JsonResponse
from django.core import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt


def createUser(request):
    respData = {}
    if request.method == "POST":
        newUserData = json.loads(request.body)
        user = User.objects.create_user(
            first_name=newUserData['first_name'],
            last_name=newUserData['last_name'],
            email=newUserData['email'],
            password=newUserData['password'],
            username=newUserData['username']
        )
        customer = Customer(email=newUserData['email'], user=user)
        cart = Cart.objects.filter(owner=customer).first()
        if not cart:
            cart = Cart.objects.create(owner=customer)
        customer.save()
        cart.save()
        respData['msg'] = "Welcome " + user.first_name + " ! "
        respData['userInfo'] = str(
            user.first_name) + " " + str(user.last_name) + " (" + str(user.id) + ")"
        respData['userId'] = str(user.id)
    else:
        respData['msg'] = "Error!"
    return JsonResponse(respData, safe=False)


def updateUser(request):
    respData = {}
    if request.method == "POST":
        print("asdsd")
        newUserData = json.loads(request.body)
        user = User.objects.get(username=newUserData['username'])
        user.username = newUserData['username']
        user.first_name = newUserData['first_name']
        user.last_name = newUserData['last_name']
        user.email = newUserData['email']
        user.password = newUserData['password']
        user.save()

        respData['msg'] = user.first_name + " updated!"
    else:
        respData['msg'] = "Error"
    return JsonResponse(respData, safe=False)


def getUserDataById(request):
    user = User.objects.get(id=request.POST['user_id'])
    serialized_obj = serializers.serialize('json', [user])
    return JsonResponse(serialized_obj, safe=False)


def deleteUser(request):
    user = User.objects.get(id=request.POST['user_id'])
    customer = Customer.objects.get(user=user)
    cart = Cart.objects.create(owner=customer)
    cart.delete()
    customer.delete()
    user.delete()
    data = {
        "msg": user.first_name + " deleted"
    }
    return JsonResponse(data=data, safe=False)


def updateBalance(request):
    user = User.objects.get(id=int(request.POST['userId']))
    data = {
        "user": {
            "fname": user.first_name,
            "lname": user.last_name,
            "balance": user.player.balance
        },
        "balanceChange": request.POST['balanceDifference'],
        "newBalance": int(request.user.player.balance) + int(request.POST['balanceDifference'])
    }
    user.player.balance += int(request.POST['balanceDifference'])
    if int(request.POST['balanceDifference']) > 0:
        user.player.win += int(request.POST['balanceDifference'])
    else:
        user.player.lost += int(request.POST['balanceDifference'])
    user.save()
    user.player.save()
    return JsonResponse(data=data, safe=False)
