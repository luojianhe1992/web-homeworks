from django.shortcuts import render

# allow us to redirect
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse
from django.template import RequestContext, loader

# import the User class in models.py
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# import the auth.models User
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from grumblr.models import *



# registration is normal route, and login is login is "django.contrib.views.login"
def registration(request):
    errors = []
    context = {}
    if request.method == "GET":
        return render(request, 'grumblr/registration.html', context)

    # add 'errors' attribute to the context
    context['errors'] = errors

    password1 = request.POST['password']
    password2 = request.POST['password_confirmation']

    if password1 != password2:

        print("Passwords did not match.")

        # error1 happens
        errors.append("Passwords did not match.")

    if len(User.objects.all().filter(username = request.POST['user_name'])) > 0:
        print("Username is already taken.")

        # error2 happens
        errors.append("Username is already taken.")

    if errors:
        return render(request, 'grumblr/registration.html', context)

    # create a new user from the valid form data, using create_user function with 2 arguments, 'username' and 'password'
    new_user = User.objects.create_user(username=request.POST['user_name'], password=request.POST['password'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
    new_user.save()

    # using 'authenticate' function
    new_user = authenticate(username = request.POST['user_name'], password = request.POST['password'])

    # using 'login' function
    login(request, new_user)

    # using 'redirect' function
    return redirect('/profile/')

# python decorator to check if the user login.
@login_required
def home(request):
    print("***************************")
    print(request)
    print("***************************")
    context = {}
    # in the home page, contain all messages from all users
    all_messages = Message.objects.all().order_by('-date_time')
    context['all_messages'] = all_messages
    user = request.user
    context['user'] = user
    return render(request, 'grumblr/home.html', context)

def post_message_home_page(request):
    print("in the post_message_home_page")
    print(request)
    message_errors = []
    context = {}
    if not 'message_text' in request.POST or not request.POST['message_text']:
        message_errors.append("You must enter some messages to post.")
    else:
        message_text = request.POST['message_text']
        message_user = request.user

        # add new Message object to the data base, and the time is default to be now
        new_message = Message(text = message_text, user = message_user)
        new_message.save()

    # in the home page, the messages should contain all messages from all users
    all_messages = Message.objects.all().order_by('-date_time')
    context['all_messages'] = all_messages
    context['message_errors'] = message_errors
    return render(request, 'grumblr/home.html', context)


@login_required
def profile(request):

    context = {}

    print("this is a get request from profile.")

    print(request.user)
    context['user'] = request.user

    # in the profile page, the messages only contains the messages belongs to the user
    all_messages = Message.objects.all().filter(user = request.user).order_by('-date_time')
    context['all_messages'] = all_messages

    return render(request, 'grumblr/profile.html', context)

# go to other's profile page
def other_user_profile(request, user_id):
    context = {}
    print("go to other's profile page")

    user = User.objects.all().get(id = user_id)
    context['user'] = user

    all_messages = Message.objects.all().filter(user = user).order_by('-date_time')
    context['all_messages'] = all_messages

    return render(request, 'grumblr/profile.html', context)




# python decorator to check if the user login.
@login_required
def post_message_profile_page(request):
    message_errors = []
    context = {}
    if not 'message_text' in request.POST or not request.POST['message_text']:
        message_errors.append("You must enter some messages to post.")
    else:
        message_text = request.POST['message_text']
        message_user = request.user


        # add new Message object to the data base
        new_message = Message(text = message_text, user = message_user)
        new_message.save()

    # in the profile page, the messages only contain messages that belongs to the user
    all_messages = Message.objects.all().filter(user = request.user).order_by('-date_time')
    context['all_messages'] = all_messages
    context['message_errors'] = message_errors
    return render(request, 'grumblr/profile.html', context)




# def logout view
def my_logout(request):
    logout(request)
    return redirect('/login/')