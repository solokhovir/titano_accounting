"""titano_accounting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import path

from web import views

urlpatterns = [
    path('login', views.login),
    path('log_out', views.logged_out),
    path('', views.index),
    # path('publications/<int:number>', views.publication),
    path('product', views.product),
    path('details', views.details),
    path('materials', views.materials),
    path('product_total', views.product_total),
    path('detail_total', views.detail_total),
    path('materials_total', views.material_total),
    path('general_table', views.general_table),
    path('delete_product/<int:id>/', views.delete_product),
    path('delete_detail/<int:id>/', views.delete_detail),
    path('delete_material/<int:id>/', views.delete_material),
    path('delete_general_product/<int:id>/', views.delete_general_product),
    path('delete_general_detail/<int:id>/', views.delete_general_detail),
    path('delete_general_material/<int:id>/', views.delete_general_material),
]
