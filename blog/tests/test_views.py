from django.urls import reverse
from django.test import TestCase, Client, RequestFactory
from blog.models import Blog, BlogComment
from django.contrib.auth.models import User
from django.db.models import Q
from blog.views import (
    blog_favorite,
    blog_comment,
    update_blog_comment,
    delete_blog_comment,
    blog_comment_like,
    all_user_favorites,
    all_user_comments
)


class TestBlogViews(TestCase):
    """
    Test setup for testing blog view functions.
    """
    def setUp(self):
        self.client = Client()

        self.factory = RequestFactory()
        
        self.user = User.objects.create(
            username="testusername",
            email="test@test.com",
            first_name="Jane",
            last_name="Smith",
            password="tester!123"
        )
        self.user.save()

        self.user2 = User.objects.create(
            username="tester",
            email="tester@test.com",
            first_name="Jane",
            last_name="Smith",
            password="tester!123"
        )
        self.user2.save()

        self.blog1 = Blog.objects.create(
            title="4 Resorts Bora Bora",
            slug="4-resorts-bora-bora",
            author=self.user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog1.favorite.add(self.user)
        self.blog1.save()

        self.blog2 = Blog.objects.create(
            title="Top Places to See in Rome",
            slug="top-places-to-see-in-rome",
            author=self.user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog2.favorite.add(self.user)
        self.blog2.save()

        self.blog3 = Blog.objects.create(
            title="5 Reasons to Visit Yellowstone",
            slug="5-reasons-to-visit-yellowstone",
            author=self.user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog3.favorite.add(self.user)
        self.blog3.save()

        self.blog4 = Blog.objects.create(
            title="featured blog",
            slug="featured-blog",
            author=self.user2,
            content="this is test content",
            status=1,
            featured=True,
            blog_img="test.jpg"
        )
        self.blog4.favorite.add(self.user2)
        self.blog4.save()

        self.blog_comment = BlogComment.objects.create(
            user=self.user,
            blog=self.blog1,
            comment="this is a comment",
        )
        self.blog_comment.likes.add(self.user2)
        self.blog_comment.save()

    def test_blog_home(self):
        """
        Test blog_home() view function returns blog posts.
        """
        response = self.client.get(reverse('blog:blog_home'))
        queryset_blogs = response.context['blogs'].count()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-home.html')
        self.assertEqual(queryset_blogs, 3)
        self.assertTrue(response.context['featured'])

    def test_blog_post(self):
        """
        Test blog_post() view function returns blog post with blog 
        favorites and blog comments.
        """
        response = self.client.get(reverse('blog:blog_post', kwargs={'slug': self.blog1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-post.html')
        self.assertTrue(response.context['blog_post'], "4 Resorts Bora Bora")
        self.assertEqual(response.context['favorites_total'], 1)
        self.assertTrue(response.context['comments'])
        self.assertEqual(response.context['comments_total'], 1)
        self.assertFalse(response.context['user_liked'])

    def test_blog_favorite_remove(self):
        """
        Test blog_favorite() view function removes user blog favorite.
        """
        self.client.force_login(self.user)
        request = self.factory.get('blog/favorite/<int:pk>/', HTTP_REFERER='blog/favorite/<int:pk>/')
        request.user = self.user
        response = blog_favorite(request, self.blog1.id)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.blog1.favorite.filter(id=self.user.id))

    def test_blog_favorite_add(self):
        """
        Test blog_favorite() view function adds user blog favorite.
        """
        self.client.force_login(self.user2)
        request = self.factory.get('blog/favorite/<int:pk>/', HTTP_REFERER='blog/favorite/<int:pk>/')
        request.user = self.user2
        response = blog_favorite(request, self.blog1.id)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.blog1.favorite.filter(id=self.user2.id))

    def test_blog_comment_GET(self):
        """
        Test blog_comment() view function retrieves template/form.
        """
        self.client.force_login(self.user)
        request = self.factory.get('<str:slug>/comment/', kwargs={'slug': self.blog1.slug})
        request.user = self.user
        response = blog_comment(request, slug=self.blog1.slug)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-post.html')
        self.assertEqual(response.context['form'], 1)

    def test_blog_comment_POST(self):
        """
        Test blog_comment() view function posts comment to blog.
        """
        self.client.force_login(self.user)
        request = self.factory.post('<str:slug>/comment/', kwargs={'slug': self.blog1.slug})
        request.user = self.user
        response = blog_comment(request, slug=self.blog1.slug)
        self.assertEqual(response.status_code, 302)
        
    def test_update_blog_comment_GET(self):
        """
        Test update_blog_comment() view function retrieves template/form.
        """
        self.client.force_login(self.user)
        request = self.factory.get('<str:slug>/comment-update/', kwargs={'slug': self.blog1.slug})
        request.user = self.user
        response = update_blog_comment(request, slug=self.blog1.slug)
        self.assertEqual(response.status_code, 200)

    def test_update_blog_comment_POST(self):
        """
        Test update_blog_comment() view function updates blog post comment.
        """
        self.client.force_login(self.user)
        request = self.factory.post('<str:slug>/comment-update/', kwargs={'slug': self.blog1.slug})
        request.user = self.user
        response = blog_comment(request, slug=self.blog1.slug)
        self.assertEqual(response.status_code, 302)

    def test_delete_blog_comment(self):
        """
        Test delete_blog_comment() view function deletes user's comment.
        """
        self.client.force_login(self.user)
        request = self.factory.get('<str:slug>/comment-delete/', kwargs={'slug': self.blog1.slug})
        request.user = self.user
        response = delete_blog_comment(request, slug=self.blog1.slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.blog_comment.filter(Q(id=self.user.id) & Q(blog=self.blog1).exists()))
        
    def test_blog_activity(self):
        """
        Test blog_activity() view function returns context data.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:blog_activity'))
        self.assertEqual(response.context['comments_total'], 1)
        self.assertEqual(response.context['favorites_total'], 3)
        self.assertTrue(response.context['latest_comments'])
        self.assertTemplateUsed(response, 'blog/blog-activity.html')

    def test_all_users_favorites(self):
        """
        Test all_users_favorites() view function returns 'favorites' context data.
        """
        self.client.force_login(self.user)
        request = self.factory.get('user-favorites/')
        request.user = self.user
        response = all_user_favorites(request)
        self.assertEqual(response.status_code, 200)

    def test_all_user_comments(self):
        """
        Test all_users_comments() view function returns 'comments' context data.
        """
        self.client.force_login(self.user)
        request = self.factory.get('user-comments/')
        request.user = self.user
        response = all_user_comments(request)
        self.assertEqual(response.status_code, 200)

    def test_blog_comment_like_remove(self):
        """
        Test blog_comment_like() view function removes user's like to comment.
        """
        self.client.force_login(self.user2)
        request = self.factory.get('comment-like/<int:pk>/', HTTP_REFERER='comment-like/<int:pk>/')
        request.user = self.user2
        response = blog_comment_like(request, self.blog_comment.id)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.blog_comment.likes.filter(id=self.user2.id))

    def test_blog_comment_like_add(self):
        """
        Test blog_comment_like() view function adds user's like to comment.
        """
        self.client.force_login(self.user)
        request = self.factory.get('comment-like/<int:pk>/', HTTP_REFERER='comment-like/<int:pk>/')
        request.user = self.user
        response = blog_comment_like(request, self.blog_comment.id)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.blog_comment.likes.filter(id=self.user.id))
