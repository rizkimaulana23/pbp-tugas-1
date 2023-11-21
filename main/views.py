from django.shortcuts import render
from .models import Oculi
from django.http import HttpResponseRedirect
from main.forms import ProductForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_product = Oculi.objects.create(
            user = request.user,
            name = data["name"],
            region = data["region"],
            amount = int(data["amount"]),
            amount_collected = int(data["amount_collected"]),
            description = data["description"]
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
# Create your views here.
@login_required(login_url='/login')
def show_main(request):

    # Iterating through the data
    
    oculi = Oculi.objects.filter(user=request.user)
    if 'last_login' in request.COOKIES:
        last_login = request.COOKIES['last_login']
    else:
        last_login = 'N/A'  # Set a default value or handle the case when the key doesn't exist
    context = {
        'name' : request.user.username,
        'class' : "PBP-C",
        'oculus' : oculi,
        'last_login': last_login,
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)

def edit_product(request, id):
    # Get product berdasarkan ID
    product = Oculi.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def show_xml(request):
    data = Oculi.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Oculi.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Oculi.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Oculi.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def plus_product_amount(request, id):
    product = Oculi.objects.get(id=id)
    product.amount_collected += 1
    product.save()
    response = HttpResponseRedirect(reverse("main:show_main"))
    return response

def minus_product_amount(request, id):
    product = Oculi.objects.get(id=id)
    if (product.amount > 0):
        product.amount_collected -= 1
        product.save()
    response = HttpResponseRedirect(reverse("main:show_main"))
    return response

def remove_product(request, id):
    Oculi.objects.filter(pk=id).delete()
    response = HttpResponseRedirect(reverse("main:show_main"))
    return response

def get_product_json(request):
    product_item = Oculi.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':

        user = request.user
        name = request.POST.get("name")
        region = request.POST.get("region")
        amount = request.POST.get("amount")
        amount_collected = request.POST.get("amount_collected")
        description = request.POST.get("description")

        new_product = Oculi(name=name, region=region, amount=amount, amount_collected=amount_collected, description=description, user=user)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def plus_product_amount_ajax(request, id):
    product = Oculi.objects.get(pk=id)
    product.amount_collected += 1
    product.save()
    return HttpResponse(b"ADD", status=201)

@csrf_exempt
def minus_product_amount_ajax(request, id):
    product = Oculi.objects.get(pk=id)
    if (product.amount > 0):
        product.amount_collected -= 1
        product.save()
        return HttpResponse(b"CREATED", status=201)
    else :
        return HttpResponse(b"NOT CREATED", status=201)

    
@csrf_exempt
def remove_product_ajax(request, id):
    Oculi.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse("main:show_main"))