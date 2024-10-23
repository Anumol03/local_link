
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password

from myapp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from myapp.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required



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
        print(password)
        # Check if ward details match
        try:
            ward = Ward.objects.get(ward_no=ward_no, house_no=house_no, name=name)
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

        # Create the user and set inactive for admin approval
        user = CustomUser(
            username=username,
            email=email,
            name=name,
            adhar_no=adhar_no,
            ward_no=ward_no,
            house_no=house_no,
            role='citizen',
            profile_pic=profile_pic
        )
        user.set_password(password)  # Hash the password
        user.is_active = True  # User is active, but not approved yet
        user.is_approved = False  # Admin needs to approve this user
        user.save()

        messages.success(request, "Registration successful! Please wait for admin approval.")
        return redirect('login')  # Redirect to login page

    return render(request, 'register1.html')



def login_view(request):
    if request.method == 'POST':
        # Retrieve username and password from the request
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        # Authenticate user based on username and password
        user = authenticate(request, username=username, password=password)

        # If authentication is successful (user is not None)
        if user is not None:
            # Check if the user account is active and approved by admin
            if user.is_active:
                if user.is_approved:
                    # Log the user in
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect('index')  # Redirect to home page
                else:
                    messages.error(request, "Your account is not approved by admin yet.")
            else:
                messages.error(request, "Your account is inactive. Please contact support.")
        else:
            messages.error(request, "Invalid username or password.")

    # Render the login page
    return render(request, 'login.html')


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse_lazy('index'))
    else:
        form = PostForm()

    posts = Posts.objects.all()
    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'index.html', context)

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('edit_user', user_id=user.id)  # Redirect to user's profile or any other page
    else:
        form = UserEditForm(instance=user)

    return render(request, 'edit_user.html', {'form': form ,'user_id': user_id})

def profile_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    posts = Posts.objects.filter(user=user).order_by('-created_date')  # List user's posts
    return render(request, 'user__detail.html', {'user': user, 'posts': posts})
@login_required
def add_like_view(request ,*args ,**kargs):
    id =kargs.get("pk")
    post_obj =Posts.objects.get(id=id)
    post_obj.liked_by.add(request.user)
    return redirect("index")
@login_required
def add_comment_view(request ,*args ,**kargs):
    id =kargs.get("pk")
    post_obj =Posts.objects.get(id=id)
    comment =request.POST.get("comment")
    user =request.user
    Comments.objects.create(user=user ,comment_text=comment ,post=post_obj)
    return redirect("index")


@login_required
def remove_comment_view(request ,*args ,**kargs):
    id =kargs.get("pk")
    comment_obj =Comments.objects.get(id=id)
    if request.user == comment_obj.user:
        comment_obj.delete()
        return redirect("index")
    else:
        messages.error(request ,"pls contact admin")
        return redirect("signin")
# @login_required
# def change_cover_pic_view(request ,*args ,**kargs):
#     id =kargs.get("pk")
#     prof_obj =UserEditForm.objects.get(id=id)
#     for m =CoverpicForm(instance=prof_obj ,data=request.POST ,files=request.FILES)
#     if form.is_valid():
#         form.save()
#         return redirect("profiledetail" ,pk=id)
#     return redirect("profiledetail" ,pk=id)


def district(request):
    return render(request ,"district.html")


def thrissur(request):
    return render(request ,"thrissur.html")


def logout_view(request):
    logout(request)
    return redirect('login') 


def history_list_view(request):
    histories = History.objects.all()  # Fetch all history records
    return render(request, 'history_list.html', {'histories': histories})



def service_list(request):
    # Get all services
    services = Service.objects.all()
    
    # Prepare a list to hold the service data
    service_data = []
    
    for service in services:
        # Get users who have made posts for this service
        users_with_posts = CustomUser.objects.filter(service=service).prefetch_related('user_posts').distinct()

        # Structure the data
        user_posts_info = []
        for user in users_with_posts:
            posts = user.user_posts.filter(user=user)
            user_posts_info.append({
                'user': user,
                'posts': posts
            })
        
        service_data.append({
            'service': service,
            'users_with_posts': user_posts_info
        })

    return render(request, 'service_list.html', {'service_data': service_data})
