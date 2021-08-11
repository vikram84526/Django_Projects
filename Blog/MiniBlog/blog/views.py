from django.shortcuts import render, HttpResponseRedirect,redirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import post
from django.contrib.auth.models import Group

# Create your views here.

def home_page(request):
    posts = post.objects.all()
    return render(request, "blog/home.html", {'posts' : posts})

def about_page(request):
    return render(request, "blog/about.html")

def contact_page(request):
    return render(request, "blog/contact.html")

def dashboard(request):
    if request.user.is_authenticated:
        posts = post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        context = {'posts':posts,'full_name':full_name, 'gps':gps }

        return render(request, "blog/dashboard.html",context)
    else:
        return redirect('login')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! You have become an Author')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, "blog/signup.html", {'form': form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request, 'Logged in Succesfully !')
                    return redirect('dashboard')
        else:
            form = LoginForm()
        return render(request, "blog/login.html", {'form': form})
    else:
        return HttpResponseRedirect('dashboard')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = post(title=title, desc=desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request,'blog/addpost.html',{'form': form})
    else:
        return redirect('login')

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form': form})
    else:
        return redirect('login')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            pi.delete()
            return redirect('dashboard')
    else:
        return redirect('login')


