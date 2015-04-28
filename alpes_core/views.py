#coding: utf-8

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'inicio.html', {})

def index(request):
    return render(request,'index.html', {})

def charts(request):
    return render(request,'charts.html', {})

def pages(request):
    return render(request,'{{request}}.html', {})