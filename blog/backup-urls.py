from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('blog-activity/', views.blog_activity, name='blog_activity'),
    path('blog-activity/user-favorites/', views.all_user_favorites, name='all_user_favorites'),
    path('blog-activity/user-comments/', views.all_user_comments, name='all_user_comments'),
    path('blog-post/<str:slug>/', views.blog_post, name='blog_post'),
    path('blog-post/<str:slug>/comment/', views.blog_comment, name='blog_comment'),
    path('blog-post/comment/like/<int:pk>/', views.blog_comment_like, name='blog_comment_like'),
    path('blog-post/<str:slug>/comment/update/', views.update_blog_comment, name='update_blog_comment'),
    path('blog-post/<str:slug>/comment/delete/', views.delete_blog_comment, name='delete_blog_comment'),
    path('blog-post/<str:slug>/favorite/<int:pk>/', views.blog_favorite, name='blog_favorite'),
]