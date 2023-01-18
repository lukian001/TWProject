from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<username>/', views.user_view, name="user_account"),
    path('login', views.login_view, name="login"),
    path('signup', views.register_view, name="signup"),
    path('logout', views.logout_view, name="logout"),
    path('<username>/change_user/', views.change_user, name="change_user"),
    path('<username>/liked_posts/', views.liked_posts, name="liked_posts"),
    path('add_friend/<user_to_username>', views.add_friend, name="add_friend"),
    path('remove_friend/<user_to_username>', views.remove_friend, name="remove_friend"),
    path('accept_friend/<request_id>', views.accept_friend, name="accept_friend_request"),
    path('decline_friend/<request_id>', views.decline_friend, name="decline_friend_request")
]
