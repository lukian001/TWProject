from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from PIL import Image

from posts.models import Post
from .models import is_member as member
from .models import is_admin as admin
from .forms import CreateGroupForm, ChangeGroupForm


def create_group(request):
    if request.method == 'POST':
        create_form = CreateGroupForm(request.POST)
        if create_form.is_valid():
            group = create_form.save()
            group.groupprofile.name = group.name
            group.user_set.add(request.user)
            group.groupprofile.owner = request.user
            group.save()
            return redirect('accounts:user_account', username=request.user.username)
    else:
        create_form = CreateGroupForm()
    return render(request, 'groups/create_group.html', {'create_form': create_form})


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


def group_page(request, group_name):
    group = Group.objects.get(name=group_name)
    user = User.objects.get(username=request.user.username)
    is_member = member(user, group)
    is_admin = admin(user, group)
    posts = Post.objects.filter(host_group=group).order_by('-date')
    change_form = ChangeGroupForm(initial={
        'name': group.name,
        'description': group.groupprofile.description,
        'media': group.groupprofile.avatar
    })
    return render(request, 'groups/group_page.html', {'group': group,
                                                      'posts': posts,
                                                      'is_member': is_member,
                                                      'is_admin': is_admin,
                                                      'change_form': change_form,
                                                      })


def enter_group(request, group_name):
    group = Group.objects.get(name=group_name)
    group.user_set.add(User.objects.get(username=request.user.username))
    return redirect('groups:group_page', group_name=group_name)


def leave_group(request, group_name):
    group = Group.objects.get(name=group_name)
    group.user_set.remove(User.objects.get(username=request.user.username))
    return redirect('groups:group_page', group_name=group_name)


def change_group(request, group_name):
    if request.method == 'POST':
        group = Group.objects.get(name=group_name)
        change_form = ChangeGroupForm(request.POST, request.FILES)
        name = group_name
        da = group.name == request.POST["name"]
        if da:
            description = change_form.data.get('description')
            group.groupprofile.description = description
            if len(request.FILES) != 0:
                group.groupprofile.avatar = request.FILES["media"]
            group.save()
        else:
            if change_form.is_valid():
                name = change_form.cleaned_data.get('name')
                description = change_form.cleaned_data.get('description')
                group.name = name
                group.groupprofile.name = name
                group.groupprofile.description = description
                if len(request.FILES) != 0:
                    group.groupprofile.avatar = request.FILES["media"]
                group.save()
        resize_img(group.groupprofile.avatar)
    return redirect('groups:group_page', group_name=name)


def delete_group(request, group_name):
    group = Group.objects.get(name=group_name)
    group.delete()
    return redirect('homepage')


def group_members(request, group_name):
    group = Group.objects.get(name=group_name)
    user = User.objects.get(username=request.user.username)
    is_member = member(user, group)
    is_admin = admin(user, group)
    members = group.user_set.all()
    change_form = ChangeGroupForm(initial={
        'name': group.name,
        'description': group.groupprofile.description,
        'media': group.groupprofile.avatar
    })
    return render(request, 'groups/group_members.html', {'group': group,
                                                         'is_member': is_member,
                                                         'members': members,
                                                         'is_admin': is_admin,
                                                         'change_form': change_form,
                                                         })
