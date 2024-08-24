from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def contact(request):
    return render(request, 'catalog/contact.html')


def product_detail(request):
    return None