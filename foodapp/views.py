from django.shortcuts import render,redirect
from foodapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django import forms


# Create your views here.
@login_required
def index(request):
    photo = Photo.objects.all()
    item_list = Item.objects.all()
    if request.GET.get('search'):
        item_list = item_list.filter(item_name__icontains=request.GET.get('search'))
    context = {
        'photo': photo,
        'item_list': item_list,
    }
    


    return render(request, 'index.html', context)

@login_required
def detail(request,item_id):
    item=Item.objects.get(pk=item_id)
    context={
        'item':item,
    }
    return render(request,'details.html',context)

@login_required
def about(request):
    ab=About.objects.all()
    context={
        'ab':ab,
    }
    return render(request,'about.html',context)

@login_required
def home(request):
    item=Item.objects.all()
    context={
        'item':item,
    }
    return render(request,'home.html',context)


@login_required
def add_item(request):
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        item_desc = request.POST.get('item_desc')
        item_price = request.POST.get('item_price')
        item_image = request.FILES.get('item_image')
        
        # Initialize a new Item object
        item = Item(item_name=item_name, item_desc=item_desc, item_price=item_price)
        
        if item_image:
            item.item_image=item_image

        item.save()
        return redirect('/home/')
    
    return render(request, 'add.html')



@login_required
def update_item(request,id):
    item=Item.objects.get(id=id)
    context={
        'item':item
    }

    if request.method=="POST":
        item_name=request.POST.get('item_name')
        item_desc=request.POST.get('item_desc')
        item_price=request.POST.get('item_price')
        item_image=request.FILES.get('item_image')

        item.item_name=item_name
        item.item_desc=item_desc
        if item_image:
            item.item_image=item_image

        item.save()
        return redirect('/index/')

    return render(request,'update.html',context)


@login_required
def delete_item(request,id):
    item=Item.objects.get(id=id)

    if request.method=='POST':
        item.delete()
        return redirect('/home/')
    return render(request,'delete.html')




def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/index/')  # Correct redirection using URL name
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')



def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('/register/')  # Redirect to the registration page with an error message

        # Create a new user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, 'Registration successful. Please log in.')
        return redirect('/login/')  # Redirect to the login page after successful registration

    return render(request, 'register.html')


@login_required
def profile(request):
    profile_instances=Profile.objects.all()
    context={
        'profile_instances':profile_instances
    }
    return render(request,'profile.html',context)




@login_required
def profile_update(request):
    try:
        # Get the profile instance of the current user
        profile_instance = request.user.profile
    except ObjectDoesNotExist:
        # If the profile doesn't exist, create a new one
        profile_instance = Profile.objects.create(user_instance=request.user)
    
    # Define the ProfileForm class directly in the view
    class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ['image', 'bio', 'date_of_birth', 'education']

    if request.method == "POST":
        # Create form instance with the POST data and profile instance
        form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()
            return redirect('/profile/')  # Redirect to the profile page after successful update
    else:
        # Create form instance with the profile instance
        form = ProfileForm(instance=profile_instance)
    
    return render(request, 'profile_form.html', {'form': form})