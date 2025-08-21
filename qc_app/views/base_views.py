from django.shortcuts import render

def home(request):
    """首页视图"""
    return render(request, 'qc_app/home.html')

def base(request):
    """基础模板视图"""
    return render(request, 'base.html')
