from typing import ContextManager
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from news.forms import CommentForm
import random

# Create your views here.

def home(request):
    categorys = Category.objects.all()
    news = New.objects.all()
    latest_post = []
    latest_post1 = []
    top_post = []
    trending = random.sample(list(news), 6)

    for i in news:
        if len(top_post) < 5:
            top_post.append(i)

    for i in range(len(news)-1, -1, -1):
        if len(latest_post) < 5:
            latest_post.append(news[i])
        if len(latest_post1) < 3:
            latest_post1.append(news[i])


    context = {
        "Trending" : trending,
        "Top_post" : top_post,
        "Latest_post" : latest_post1,
        "Latest_post_1" : latest_post[0],
        "Latest_post_2" : latest_post[1],
        "Latest_post_3" : latest_post[2],
        "Latest_post_4" : latest_post[3],
        "Latest_post_5" : latest_post[4],
        "Categorys" : categorys
    }
    return render(request, 'index.html', context)

def category(request, id):
    categorys = Category.objects.all()
    arr = New.objects.all()
    top_post , last_post = [], []
    for i in arr:
        if i.category.id == id :
            if len(top_post) < 4:
                top_post.append(i)
    for i in range(len(arr)-1, -1, -1):
        if len(last_post) < 3:
            last_post.append(arr[i])
    context = {
        "Categorys" : categorys,
        "news" : arr,
        "top_Post" : top_post,
        "last_Post" : last_post
    }
    return render(request, 'category.html', context)

def blog(request):
    categorys = Category.objects.all()
    context = {
        "Categorys" : categorys
    }
    return render(request, 'blog.html', context)

def blog_details(request):
    categorys = Category.objects.all()
    context = {
        "Categorys" : categorys
    }

    return render(request, 'blog_details.html', context)

def about(request):
    categorys = Category.objects.all()
    context = {
        "Categorys" : categorys
    }
    return render(request, 'about.html', context)

def contact(request):
    categorys = Category.objects.all()
    context = {
        "Categorys" : categorys
    }
    return render(request, 'contact.html', context)

def elements(request):
    categorys = Category.objects.all()
    context = {
        "Categorys" : categorys
    }
    return render(request, 'elements.html', context)
 
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password is incorrect")
    return render(request, 'signin.html')
def sendMail(request):
    usernames = User.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        # email = request.POST['email']
        # pass1 = request.POST['pass1']
        # pass2 = request.POST['pass2']
        check = 0
        # if pass1 != pass2:
        #     messages.error(request, "Passwords didn't match!")
        #     return render(request, 'sendMail.html')
        # else:
        for i in usernames:
            if i.username == username:
                check = 1
                messages.success(request, "Vui long check mail")
                break;
        if check == 0:
        #     myuser = User.objects.create_user(username=username, email=email, password=pass1)
        #     myuser.save()

            messages.error(request, "Your email not exist")
            return redirect('signin')

    return render(request, 'sendMail.html')
def logoutUser(request):
    logout(request)
    return redirect('home')
#@login_required(login_url='signin')
def sign_up(request):
    usernames = User.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        check = 0
        if pass1 != pass2 :
            messages.error(request,  "Passwords didn't match!")
            return render(request, 'sin-up.html')
        else:
            for i in usernames:
                if i.username == username:
                    check = 1
                    messages.error(request, "Username has been existed.")
                    break;
            if check == 0:             
                myuser = User.objects.create_user(username=username,email=email,password=pass1) 
                myuser.save()

                messages.success(request, "Your account has been successfully created.")
                return redirect('signin')

    return render(request, 'sin-up.html')
#@login_required(login_url='login')

def my_Main(request):
    categorys = Category.objects.all()
    context = {
        "Categorys" : categorys
    }
    return render(request, 'main.html', context)

def post_details(request, id):
    categorys = Category.objects.all()
    new = New.objects.get(pk=id)
    Cmt = Comment.objects.all()
    arr = []
    for i in Cmt:
        if i.new.id == id:
            arr.append(i)
        print(i)
    form = CommentForm()
    context = {
        "Categorys" : categorys,
        "new" : new,
        "form" : form,
        "Cmt" : arr
    }
    if request.method == "POST":
        form = CommentForm(request.POST, author= request.user, new=new)
        if form.is_valid():
           form.save()
           return HttpResponseRedirect(request.path)
    return render(request, 'post_details.html', context)

def feedback(request):
    if request.method == 'POST':
        message = request.POST['message']
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        Feedback.objects.create(message=message, name=name, email=email, subject=subject)
        return render(request, 'feedback.html')
    return redirect('/contact')

def search(request):

    news = New.objects.all()
    last_post = []
        
    for i in range(len(news)-1, -1, -1):
        if len(last_post) < 3:
            last_post.append(news[i])

    print(request.method)
    if request.method == 'GET':
        try:
            search = request.GET['search'].lower().split()
        except:
            return redirect('/')

        res  = []
        for new in news:
            for text in search:
                if text in new.title.lower():
                    res.append(new)
                    break
        return render(request,'search.html', {'news':res, 'search':request.GET['search'], 'last_Post' : last_post})
    return redirect('/', {'last_Post' : last_post})

