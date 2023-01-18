from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from posts.models import Post
from groups.forms import CreateGroupForm
from .models import FriendRequest
from PIL import Image

from .forms import CreateUserForm, ChangeUserForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        user_form = AuthenticationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        signup_form = CreateUserForm()
        user_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'user_form': user_form,
                                                   'signup_form': signup_form})


def register_view(request):
    signup_form = CreateUserForm(request.POST)

    signup_form.fields['email'].required = True

    if signup_form.is_valid():
        user = signup_form.save()
        login(request, user)
        return redirect('accounts:user_account', user.username)
    else:
        user_form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'user_form': user_form,
                                                       'signup_form': signup_form})


def user_view(request, username):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        is_friend = user.groups.filter(
            name=str(request.user.id) + request.user.username + str(request.user.id)).exists()
        request_sent = FriendRequest.objects.filter(user_from=request.user,
                                                    user_to=user).exists() or FriendRequest.objects.filter(
            user_from=user, user_to=request.user).exists()
        group_form = CreateGroupForm()
        change_form = ChangeUserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'description': user.profile.description,
            'media': user.profile.avatar
        })
        return render(request, 'accounts/user.html', {'user': user,
                                                      'group_form': group_form,
                                                      'posts': Post.objects.filter(owner=user).order_by('-date'),
                                                      'is_friend': is_friend,
                                                      'request_sent': request_sent,
                                                      'change_form': change_form})
    else:
        return render(request, 'error_page.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')


def add_friend(request, user_to_username):
    if request.method == 'POST':
        user_to = User.objects.get(username=user_to_username)
        friend_request = FriendRequest(user_from=request.user, user_to=user_to)
        friend_request.save()
    return redirect('accounts:user_account', username=user_to_username)


def accept_friend(request, request_id):
    if request.method == "POST":
        fr = FriendRequest.objects.get(id=request_id)
        user_from = fr.user_from
        user_to = fr.user_to
        groupTo = Group.objects.get(name=str(user_to.id) + user_to.username + str(user_to.id))
        groupFrom = Group.objects.get(name=str(user_from.id) + user_from.username + str(user_from.id))
        groupFrom.user_set.add(user_to)
        groupTo.user_set.add(user_from)
        fr.delete()
    return render(request, 'main_page.html')


def decline_friend(request, request_id):
    if request.method == "POST":
        fr = FriendRequest.objects.get(id=request_id)
        fr.delete()
    return render(request, 'main_page.html')


def remove_friend(request, user_to_username):
    if request.method == 'POST':
        user = User.objects.get(username=user_to_username)
        user_group = Group.objects.get(name=str(user.id) + user.username + str(user.id))
        user_group.user_set.remove(request.user)
        user_group = Group.objects.get(name=str(request.user.id) + request.user.username + str(request.user.id))
        user_group.user_set.remove(user)
    return redirect('accounts:user_account', username=user_to_username)


def resize_img(pimg):
    img = Image.open(pimg.path)
    if img.height > img.width:
        left = 0
        right = img.width
        top = (img.height - img.width) / 2
        bottom = (img.height + img.width) / 2
        img = img.crop((left, top, right, bottom))
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(pimg.path)

    elif img.width > img.height:
        left = (img.width - img.height) / 2
        right = (img.width + img.height) / 2
        top = 0
        bottom = img.height
        img = img.crop((left, top, right, bottom))
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(pimg.path)


def change_user(request, username):
    if request.method == "POST":
        user = User.objects.get(username=username)
        change_form = ChangeUserForm(request.POST, request.FILES)
        if change_form.is_valid():
            user.first_name = change_form.cleaned_data.get('first_name')
            user.last_name = change_form.cleaned_data.get('last_name')
            user.profile.description = change_form.cleaned_data.get('description')
            if len(request.FILES) != 0:
                user.profile.avatar = request.FILES["media"]
            user.save()
            resize_img(user.profile.avatar)
    return redirect('accounts:user_account', username=username)


def liked_posts(request, username):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        is_friend = user.groups.filter(
            name=str(request.user.id) + request.user.username + str(request.user.id)).exists()
        request_sent = FriendRequest.objects.filter(user_from=request.user,
                                                    user_to=user).exists() or FriendRequest.objects.filter(
            user_from=user, user_to=request.user).exists()
        group_form = CreateGroupForm()
        change_form = ChangeUserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'description': user.profile.description,
            'media': user.profile.avatar
        })
        return render(request, 'accounts/user.html', {'user': user,
                                                      'group_form': group_form,
                                                      'posts': user.profile.liked_posts.order_by('-date'),
                                                      'is_friend': is_friend,
                                                      'request_sent': request_sent,
                                                      'change_form': change_form})
    else:
        return render(request, 'error_page.html')
