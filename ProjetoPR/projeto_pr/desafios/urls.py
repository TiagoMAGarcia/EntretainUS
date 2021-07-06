from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import path

app_name = 'desafios'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login_user'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.log_out, name='logout'),
    path('user_homepage/', views.user_homepage, name='user_homepage'),
    path('<str:challenge_type>/create_challenge/', views.create_challenge, name='create_challenge'),
    path('<str:challenge_type>/challenges/', views.challenges_views, name='challenges'),
    path('<str:challenge_type>/challenges/like_up/', views.challenge_like_upvote, name='challenge_like_upvote'),
    path('<str:challenge_type>/challenges/like_down/', views.challenge_like_downvote, name='challenge_like_downvote'),
    path('challenges/<str:challenge_tag>/comments', views.comments, name='comments'),
    path('challenges/<str:challenge_tag>/post_comment', views.post_comment, name='post_comment'),

]
