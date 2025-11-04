from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .models import User, Token
from .tasks import send_registration_email, send_reset_email
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        user, created = User.objects.get_or_create(email=email)
        token = Token.generate_token(user, 'register')
        send_registration_email.delay(email, token)
        return render(request, 'email_sent.html')
    return render(request, 'register.html')

def set_password(request, token):
    try:
        token_obj = Token.objects.get(token=token, token_type='register')
        if token_obj.expires_at < timezone.now():
            return render(request, 'token_invalid.html')
        if request.method == 'POST':
            password = request.POST['password']
            user = token_obj.user
            user.set_password(password)
            user.is_registered = True
            user.save()
            token_obj.delete()
            return redirect('login')
        return render(request, 'set_password.html')
    except Token.DoesNotExist:
        return render(request, 'token_invalid.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            token = Token.generate_token(user, 'reset')
            send_reset_email.delay(email, token)
            return render(request, 'email_sent.html')
        except User.DoesNotExist:
            return render(request, 'register.html')  # Или ошибка
    return render(request, 'forgot_password.html')

def reset_password(request, token):
    try:
        token_obj = Token.objects.get(token=token, token_type='reset')
        if token_obj.expires_at < timezone.now():
            return render(request, 'token_invalid.html')
        if request.method == 'POST':
            password = request.POST['password']
            user = token_obj.user
            user.set_password(password)
            user.save()
            token_obj.delete()
            return redirect('login')
        return render(request, 'reset_password.html')
    except Token.DoesNotExist:
        return render(request, 'token_invalid.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Добавьте home view
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
