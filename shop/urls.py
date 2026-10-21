from django.urls import path
from . import views

urlpatterns = [
    path('', views.vuln_search, name='home'),
    path('safe-search/', views.fixed_search, name='safe_search'),
    path('login/', views.vuln_login, name='login'),
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile, name='profile'),
]