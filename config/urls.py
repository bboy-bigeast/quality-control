"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from qc_app import views

urlpatterns = [
    #基础模板
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('base/', views.base, name='base'),
    #干膜模板
    path('dryfilm/', views.dryfilm_list, name='dryfilm_list'),
    path('dryfilm/create/', views.dryfilm_create, name='dryfilm_create'),
    path('dryfilm/edit/<uuid:pk>/', views.dryfilm_edit, name='dryfilm_edit'),
    path('dryfilm/delete/', views.dryfilm_delete, name='dryfilm_delete'),
    #干膜标准模板
    path('dryfilm/standard/create', views.create_dryfilm_standard, name='create_dryfilm_standard'),
    path('dryfilm/standard/success/<uuid:pk>/', views.success_view, name='dryfilm_success'),
    path('dryfilm/standard/list', views.dryfilm_standard_list, name='dryfilm_standard_list'),
    path('dryfilm/standard/edit/<str:product_name>/', views.dryfilm_standard_edit, name='dryfilm_standard_edit'),
    path('dryfilm/standard/delete/', views.dryfilm_standard_delete, name='dryfilm_standard_delete'),
    
 
    #胶粘剂模板
    path('adhesive/', views.adhesive_list, name='adhesive_list'),
    path('adhesive/create/', views.adhesive_create, name='adhesive_create'),
    path('adhesive/edit/<uuid:pk>/', views.adhesive_edit, name='adhesive_edit'),
    path('adhesive/delete/', views.adhesive_delete, name='adhesive_delete'),
    #原料模板
    path('rawmaterial/', views.rawmaterial_list, name='rawmaterial_list'),
    path('rawmaterial/create/', views.rawmaterial_create, name='rawmaterial_create'),
    path('rawmaterial/edit/<uuid:pk>/', views.rawmaterial_edit, name='rawmaterial_edit'),
    path('rawmaterial/delete/', views.rawmaterial_delete, name='rawmaterial_delete'),
    #小试模板
    path('trialproduct/', views.trialproduct_list, name='trialproduct_list'),
    path('trialproduct/create/', views.trialproduct_create, name='trialproduct_create'),
    path('trialproduct/edit/<uuid:pk>/', views.trialproduct_edit, name='trialproduct_edit'),
    path('trialproduct/delete/', views.trialproduct_delete, name='trialproduct_delete'),
    #报告中心模板
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/edit/<uuid:pk>/', views.report_edit, name='report_edit'),
    path('reports/delete/', views.report_delete, name='report_delete'),
    #分析中心模板
    path('analysis/', views.analysis_list, name='analysis_list'),
    path('analysis/create/', views.analysis_create, name='analysis_create'),
    path('analysis/edit/<uuid:pk>/', views.analysis_edit, name='analysis_edit'),
    path('analysis/delete/', views.analysis_delete, name='analysis_delete'),

]
