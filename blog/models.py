from django.conf import settings
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    """
    Blog model for featured/non-featued blog posts.
    """
    class BlogPublishedObjects(models.Manager):
        """
        BlogObjects manager returns only blog posts with status set
        to publish.
        """
        def get_queryset(self):
            return super().get_queryset().filter(status=1)

    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, related_name="authored", on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    featured = models.BooleanField(default=False)
    blog_img = models.ImageField(upload_to='blog/')
    favorite = models.ManyToManyField(User, related_name="blog_favorites", blank=True)

    objects = models.Manager()
    blog_published = BlogPublishedObjects()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    """
    BlogComment model for comments made on blog posts.
    """
    user = models.ForeignKey(User, related_name="commented", on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name="blog_comments", on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name="comment_likes", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True) 

    def has_user_commented(user_id, blog_id):
        """
        Method determines if a user has commented on a blog post.
        """
        try:
            comment = BlogComment.objects.get(Q(user=user_id) & Q(blog=blog_id))
            if comment:
                return True
        except:
            return False
