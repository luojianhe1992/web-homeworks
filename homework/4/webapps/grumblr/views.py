from django.shortcuts import render


# allow us to redirect
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import Http404
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

# import the User class in models.py
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import *

# import the auth.models User
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from grumblr.models import *

from grumblr.forms import *

from mimetypes import guess_type

from django.core.mail import send_mail



# registration is normal route, and login is login is "django.contrib.views.login"
def registration(request):

    print("in the registration function.")

    context = {}

    if request.method == "GET":
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/registration.html', context)

    form = RegistrationForm(request.POST)


    print(form)

    context['form'] = form

    # using form to do the validation job
    if not form.is_valid():
        print("the RegistrationForm object is not valid")
        return render(request, 'grumblr/registration.html', context)


    # create a new user from the valid form data, using create_user function with 2 arguments, 'username' and 'password'
    new_user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'])
    new_user.save()

    # create a new profile
    new_profile = Profile(user = new_user, first_name = new_user.first_name, last_name = new_user.last_name)
    new_profile.save()

    # create a new friendship
    new_friendship = Friendship(user = new_user)
    new_friendship.save()

    # using 'authenticate' function
    new_user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])

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

    user_profile = Profile.objects.all().get(user = user)

    context['user_profile'] = user_profile


    print("***************************")
    print(user_profile)
    print(user_profile.picture)
    print("***************************")


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

    user_profile = Profile.objects.all().get(user = request.user)

    context['user_profile'] = user_profile

    return render(request, 'grumblr/home.html', context)


@login_required
def profile(request):

    context = {}

    print("this is a get request from profile.")

    print(request.user)

    user = request.user

    context['user'] = user

    # in the profile page, the messages only contains the messages belongs to the user
    all_messages = Message.objects.all().filter(user = request.user).order_by('-date_time')
    context['all_messages'] = all_messages

    user_profile = get_object_or_404(Profile, user = user)


    print("this is a get request for the profile page.")

    profile_form = ProfileForm(instance=user_profile)
    context['profile_form'] = profile_form

    return render(request, 'grumblr/profile.html', context)


# go to other's profile page
def other_user_profile(request, user_id):

    print(request)
    print(request.method)
    print(user_id)

    context = {}
    print("go to other's profile page")

    login_user = request.user

    user = User.objects.all().get(id = user_id)
    context['user'] = user

    current_user_profile = Profile.objects.all().get(user = user)

    current_user_profile_id = current_user_profile.id
    context['current_user_profile_id'] = current_user_profile_id


    print("request user id is: ")
    print(request.user.id)
    print("click user id is: ")
    print(user_id)


    if request.user == User.objects.all().get(id = user_id):
        other_user = False
    else:
        other_user = True


    print('other_user is :')
    print(other_user)

    context['other_user'] = other_user

    all_messages = Message.objects.all().filter(user = user).order_by('-date_time')
    context['all_messages'] = all_messages

    user_profile = get_object_or_404(Profile, user = user)
    print("this is a get request for the profile page.")
    profile_form = ProfileForm(instance=user_profile)
    context['profile_form'] = profile_form

    print("*************************")
    print(profile_form)
    print("*************************")

    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(context['other_user'])

    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    # content_type = guess_type(user_profile.picture.name)
    # image_src = HttpResponse(user_profile.picture, content_type = content_type)
    #
    # # image_src = user_profile.picture
    #
    # context['image_src'] = image_src
    #
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(user_profile.picture.path)
    #
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    # print("image_src is:")
    # # print(image_src)
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    followed = False

    login_user_friendship = Friendship.objects.all().get(user = login_user)
    login_friends = login_user_friendship.friends.all()

    for login_friend in login_friends:

        print("in the for loop to check if follow or not")

        if login_friend == user:
            followed = True

    context['followed'] = followed

    other_user_id = user_id
    context['other_user_id'] = other_user_id

    print("in the end of other_user_profile function.")

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
    # return render(request, 'grumblr/profile.html', context)

    return redirect('/profile/')



# def logout view
def my_logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def go_to_profile_edit_page(request):


    context = {}

    print("this is go_to_profile_edit_page function.")

    print(request.user)

    print(request.method)

    user = request.user

    context['user'] = user

    user_profile = get_object_or_404(Profile, user = user)

    if request.method == 'GET':
        profile_form = ProfileForm(instance=user_profile)
        context['profile_form'] = profile_form
        return render(request, 'grumblr/profile_edit.html', context)

    # add profile to the context

    print("post request in the profile_edit page")

    profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile)

    if not profile_form.is_valid():

        print("profile_form is not valid.")

        context['profile_form'] = profile_form
        return render(request, 'grumblr/profile_edit.html', context)

    profile_form.save()

    return redirect(reverse('profile'))

    '''
    print(request.method)
    print(request)

    context = {}

    profile_to_edit = get_object_or_404(Profile, user = request.user)

    if request.method == 'GET':
        form = ProfileForm(instance=profile_to_edit)
        context['form'] = form
        return render(request, 'grumblr/profile_edit.html', context)

    profile_form = ProfileForm(request.POST, request.FILES, instance=profile_to_edit)

    # using form to do the validation job
    if not profile_form.is_valid():

        print("profile_form is not valide")
        context['profile_form_form'] = profile_form
        return render(request, 'grumblr/profile_edit.html', context)

    form.save()

    return render(reverse('home'))
    '''



# @login_required
# def profile_edit(reqest):
#
#     print("in the profile_edit function")
#
#     print(reqest.method)
#     print(reqest)
#
#     context = {}
#
#
#
#     user = reqest.user
#
#     current_user_profile = Profile.objects.all().get(user = user)
#
#     print("before current_user_profile is:")
#     print(current_user_profile)
#
#     current_user_profile.first_name = first_name
#     current_user_profile.last_name = last_name
#     current_user_profile.age = age
#     current_user_profile.short_bio = short_bio
#
#     print("*******************************")
#     print(current_user_profile.first_name)
#     print(current_user_profile.last_name)
#     print(current_user_profile.age)
#     print(current_user_profile.short_bio)
#     print("*******************************")
#
#
#     current_user_profile.save()
#
#     print("after current_user_profile is:")
#     print(current_user_profile)
#
#
#     return redirect( '/profile/')



@login_required
def go_to_password_change_page(request):

    print(request.method)
    print(request)

    context = {}

    user = request.user
    context['user'] = user

    return render(request, 'grumblr/change_password.html', context)

def update_password(request):
    print(request.method)

    print(request)

    context = {}

    errors = []
    context['errors'] = errors

    user = request.user
    context['user'] = user

    print("*****************************")
    print(user.password)

    new_password1 = request.POST['new_password1']
    new_password2 = request.POST['new_password2']

    if new_password1 != new_password2:
        errors.append("Two passwords do not match. Please enter again.")
        return render(request, 'grumblr/change_password.html', context)

    user.set_password(new_password1)

    print("*****************************")


    print(user.password)

    user.save()

    new_user = authenticate(username = user.username, password = new_password1)
    login(request, new_user)

    # form = PasswordChangeForm(user=user, data=request.POST)
    # if form.is_valid():
    #     form.save()
    #     update_session_auth_hash(request, form.user)
    # else:
    #     errors.append("The form is not valid.")
    #     return render(request, 'grumblr/change_password.html' , context)


    return redirect('/profile/')



# @login_required
# def upload_photo(request):
#
#     print("in the upload photo function.")
#
#     print(request.method)
#
#     print(request)
#
#     context = {}
#
#
#     print(new_user_photo)
#
#     form = User_Photo_Form(request.POST, request.FILES, instance=new_user_photo)
#
#     if not form.is_valid():
#         context['form'] = form
#         return render(request, 'grumblr/profile.html', context)
#
#     form.save()
#
#     print(form)
#
#     print("**************************")
#     print(User_Photo.objects.all())
#     print("**************************")
#
#
#
#     return redirect(reverse('profile'))


# define get_photo function
def get_photo(request):

    print("in the get_photo function")

    print(request.user)

    profile = get_object_or_404(Profile, user = request.user)

    print("****************")
    print(profile)
    print("****************")

    if not profile.picture:
        print("raise Http404.")
        raise Http404

    content_type = guess_type(profile.picture.name)

    return HttpResponse(profile.picture, content_type = content_type)

def get_other_photo(request, id):

    print("in the get_other_photo function.")

    print(request)
    print(request.method)

    current_user = User.objects.all().get(id = id)

    current_profile = Profile.objects.all().get(user = current_user)

    current_profile_id = current_profile.id

    print(current_profile_id)

    id = current_profile_id

    current_user_profile_object = get_object_or_404(Profile, id = id)

    print("********************************")
    print(current_user_profile_object)
    print("********************************")

    if not current_user_profile_object.picture:
        print("raise Http404.")
        raise Http404

    content_type = guess_type(current_user_profile_object.picture.name)

    return HttpResponse(current_user_profile_object.picture, content_type = content_type)


def get_friends_stream(request):

    print("in th get_friends_stream function")

    print(request)

    print(request.method)

    context = {}

    user_friendship = Friendship.objects.all().filter(user = request.user)

    if user_friendship == []:

        context['all_messages'] = [];

        return render(request, 'grumblr/friends_stream.html', context)

    user_friends = user_friendship[0].friends.all()

    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(user_friendship)
    print(user_friends)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    all_messages = []


    for friend in user_friends:

        print("^^^^^^^^^^^^^^^^^^^^^^")
        print(friend)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")


        friend_messages = Message.objects.all().filter(user = friend)

        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(friend_messages)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        if friend_messages:
            for friend_message in friend_messages:
                all_messages.append(friend_message)


    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    sorted_all_messages = sorted(all_messages, key=lambda Message: Message.date_time, reverse=True)
    print(sorted_all_messages)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    all_messages = sorted_all_messages

    context['all_messages'] = all_messages

    return render(request, 'grumblr/friends_stream.html', context)

def follow(request):

    print("in the follow function.")

    print("*****************************")
    print(request.POST['other_user_id'])
    print("*****************************")


    print(request)

    print(request.method)

    context = {}

    login_user = request.user

    user = User.objects.all().get(id = request.POST['other_user_id'])

    context['other_user_id'] = request.POST['other_user_id']

    context['user'] = user

    context['other_user'] = True

    all_messages = Message.objects.all().filter(user = user).order_by('-date_time')
    context['all_messages'] = all_messages

    user_profile = get_object_or_404(Profile, user = user)
    print("this is a get request for the profile page.")
    profile_form = ProfileForm(instance=user_profile)
    context['profile_form'] = profile_form


    # add profile_user to be one of the friends of login_user
    login_user_friendship = Friendship.objects.all().get(user = login_user)
    login_user_friends = login_user_friendship.friends
    login_user_friends.add(user)
    context['followed'] = True

    return render(request, 'grumblr/profile.html', context)


def unfollow(request):

    print("in the unfollow function.")

    print(request)

    print(request.method)

    context = {}

    login_user = request.user
    user = User.objects.all().get(id = request.POST['other_user_id'])
    context['other_user_id'] = request.POST['other_user_id']

    context['user'] = user
    context['other_user'] = True

    all_messages = Message.objects.all().filter(user = user).order_by('-date_time')
    context['all_messages'] = all_messages

    user_profile = get_object_or_404(Profile, user = user)
    print("this is a get request for the profile page.")
    profile_form = ProfileForm(instance=user_profile)
    context['profile_form'] = profile_form


    # add profile_user to be one of the friends of login_user
    login_user_friendship = Friendship.objects.all().get(user = login_user)
    login_user_friends = login_user_friendship.friends

    login_user_friends.remove(user)

    context['followed'] = False


    return render(request, 'grumblr/profile.html', context)


def reset_password(request):

    print("in the reset_password function.")

    print(request)
    print(request.method)

    context = {}

    if request.method == 'GET':

        form = Email_Form()

        print("*********************************")
        print(form)
        print("*********************************")

        context['form'] = form

        return render(request, 'grumblr/reset_page.html', context)


    print("this is a post request in the reset_password function.")

    form = Email_Form(request.POST)

    if not form.is_valid():
        print("the RegistrationForm object is not valid")
        return render(request, 'grumblr/registration.html', context)

    recipient_list = []
    recipient_list.append(form.cleaned_data['email'])

    send_mail(subject="Reset your password.",
              message="Please reset your password by using this email.",
              from_email = "jianhel@andrew.cmu.edu",
              recipient_list=recipient_list)


    context['email'] = form.cleaned_data['email']

    return render(request, 'grumblr/email_confirmation_information.html', context)
