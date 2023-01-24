from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from .models import Blog, User, BlogComment
from .forms import UserCommentForm


def blog_home(request):
    blogs = Blog.blog_published.filter(featured=False)
    featured = Blog.blog_published.get(featured=True)
    return render(request, 'blog/blog-home.html', {'blogs': blogs, 'featured': featured})

def blog_post(request, slug):
    blog_post = Blog.blog_published.get(slug=slug)
    user_favorited = blog_post.favorite.filter(id=request.user.id).exists()
    favorites_total = blog_post.favorite.values().count()
    comments = BlogComment.objects.filter(blog=blog_post.id)
    comments_total = BlogComment.objects.filter(blog=blog_post.id).count()

    context = {
        'blog_post': blog_post,
        'comments': comments,
        'user_favorited': user_favorited,
        'favorites_total': favorites_total,
        'comments_total': comments_total,
    }
    return render(request, 'blog/blog-post.html', context)

@login_required
def blog_favorite(request, pk):
    blog = Blog.blog_published.get(pk=pk)
    user = User.objects.get(id=request.user.id)
    if blog.favorite.filter(id=user.id):
        blog.favorite.remove(user.id)
    else:
        blog.favorite.add(user.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def blog_comment(request, slug):
    blog = Blog.blog_published.get(slug=slug)
    if request.method == "POST":
        form = UserCommentForm(request.POST)
        user_commented = BlogComment.has_user_commented(request.user.id, blog.id)
        if user_commented is True:
            messages.error(request, 'You have already commented on this blog post.')
            return redirect('blog:blog_post', slug=blog.slug)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.comment = form.cleaned_data['comment']
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('blog:blog_post', slug=blog.slug)
    else:
        form = UserCommentForm()
    return render(request, 'blog/blog-post.html', {'form': form})

@login_required
def update_blog_comment(request, slug):
    blog = Blog.blog_published.get(slug=slug)
    comment = BlogComment.objects.get(Q(user=request.user.id) & Q(blog=blog.id))
    if request.method == "POST":
        form = UserCommentForm(request.POST)
        if form.is_valid():
            comment.comment = form.cleaned_data['comment']
            comment.updated = datetime.now()
            comment.save()
            messages.success(request, "Your comment has been updated.")
            return redirect('blog:blog_post', slug=blog.slug)
    else:
        form = UserCommentForm()
    return render(request, 'blog/update-comment.html', {'form': form, 'blog': blog, 'comment': comment})

@login_required
def delete_blog_comment(request, slug):
    blog = Blog.blog_published.get(slug=slug)
    comment = BlogComment.objects.get(Q(user=request.user.id) & Q(blog=blog.id))
    comment.delete()
    messages.success(request, "Your comment has been deleted.")
    return redirect('blog:blog_post', slug=blog.slug)

@login_required
def blog_activity(request):
    comments_total = BlogComment.objects.filter(user=request.user.id).count()
    favorites_total = Blog.objects.filter(favorite=request.user.id).count()
    latest_comments = BlogComment.objects.filter(user=request.user.id).order_by('created')[0:5]
    context = {
        'comments_total': comments_total, 
        'favorites_total': favorites_total,
        'latest_comments': latest_comments
    }
    return render(request, 'blog/blog-activity.html', context) 

@login_required
def all_user_favorites(request):
    favorites = Blog.objects.filter(favorite=request.user.id)
    return render(request, 'blog/all-user-favorites.html', {'favorites': favorites})

@login_required
def all_user_comments(request):
    comments = BlogComment.objects.filter(user=request.user.id)
    return render(request, 'blog/all-user-comments.html', {'comments': comments})

@login_required
def blog_comment_like(request, pk):
    comment = BlogComment.objects.get(pk=pk)
    if comment.likes.filter(id=request.user.id):
        comment.likes.remove(request.user.id)
    else:
        comment.likes.add(request.user.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
