from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('register/', views.register_user_ssr, name='register'),
    path('login/', views.RoleBasedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]