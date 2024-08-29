

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password

from myapp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        ward_no = request.POST['ward_no']
        house_no = request.POST['house_no']
        name = request.POST['name']
        adhar_no = request.POST['adhar_no']
        profile_pic = request.FILES.get('profile_pic')

        # Check if ward details match
        try:
            ward = Ward.objects.get(ward_no=ward_no, house_no=house_no ,name=name)
        except Ward.DoesNotExist:
            messages.error(request, "Ward details do not match.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if the username or email already exists
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Username or email already exists.")
            return redirect('register')

        # Create the user but do not activate immediately
        user = CustomUser(username=username, email=email, name=name, adhar_no=adhar_no, ward_no=ward_no, house_no=house_no, role='citizen', profile_pic=profile_pic)
        user.set_password(password)
        user.is_active = False  # Set to False until admin approves
        user.save()

        messages.success(request, "Registration successful! Please wait for admin approval.")
        return redirect('login')  # Redirect to login page

    return render(request, 'register1.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()  # Remove leading/trailing spaces
        password = request.POST['password'].strip()  # Remove leading/trailing spaces
        print(username, password)

        try:
            # Retrieve the user by username
            user = CustomUser.objects.get(username=username)
            print(user)

            # Check if the password is correct
            if check_password(password, user.password):
                if user.is_active:  # Check if the user's account is active
                    if user.is_approved:  # Check if the user has been approved by an admin
                        login(request, user)
                        messages.success(request, "Login successful!")
                        return redirect('index')  # Redirect to the home page or dashboard after login
                    else:
                        messages.error(request, "Account is not approved by admin yet.")
                else:
                    messages.error(request, "Account is inactive. Please contact support.")
            else:
                messages.error(request, "Invalid username or password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def index(request):
    return render(request,'index.html')