from django.shortcuts import render, redirect
from posts.forms import CreatePostForm
from search.forms import SearchForm


def homepage(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    else:
        groups = request.user.groups

        posts = []
        for group in groups.all():
            for post in group.post_set.all()[::1]:
                posts.append(post)

        posts.sort(key=lambda pst: pst.date, reverse=True)

        post_form = CreatePostForm()
        post_form.set_choices(request.user.groups.all(), request.user.id, request.user.username)
        post_form.fields['host_group'].queryset = request.user.groups

        search_form = SearchForm()
        return render(request, 'main_page.html', {'posts': posts,
                                                  'post_form': post_form,
                                                  'search_form': search_form})


def games(request):
    if request.user.is_authenticated:
        return render(request, 'games_page.html')
    else:
        return redirect('homepage.html')
