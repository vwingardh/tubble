from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('blog-activity/', views.blog_activity, name='blog_activity'),
    path('user-favorites/', views.all_user_favorites, name='all_user_favorites'),
    path('user-comments/', views.all_user_comments, name='all_user_comments'),
    path('<str:slug>/', views.blog_post, name='blog_post'),
    path('<str:slug>/comment/', views.blog_comment, name='blog_comment'),
    path('comment-like/<int:pk>/', views.blog_comment_like, name='blog_comment_like'),
    path('<str:slug>/comment-update/', views.update_blog_comment, name='update_blog_comment'),
    path('<str:slug>/comment-delete/', views.delete_blog_comment, name='delete_blog_comment'),
    path('favorite/<int:pk>/', views.blog_favorite, name='blog_favorite'),
]
