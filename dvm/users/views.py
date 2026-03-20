from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView

User = get_user_model()

def register_user_ssr(request):

    if request.user.is_authenticated:
        if getattr(request.user, 'role', '') == 'driver':
            return redirect('driver-dashboard')
        return redirect('request-ride-ssr')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', 'passenger')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, role=role)
        

        login(request, user)
        messages.success(request, f"Welcome to the Carpool, {username}!")
        
        if role == 'driver':
            return redirect('driver-dashboard')
        return redirect('request-ride-ssr')

    return render(request, 'users/register.html')

class RoleBasedLoginView(LoginView):
    template_name = 'users/login.html'
    
    redirect_authenticated_user = True 

    def get_success_url(self):
        
        user = self.request.user
        
        if getattr(user, 'role', '') == 'driver':
            return reverse('driver-dashboard') 
        
        return reverse('request-ride-ssr')