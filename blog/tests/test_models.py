from django.test import TestCase
from blog.models import Blog, BlogComment
from django.contrib.auth.models import User 
from django.db.models import Q


class BlogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testusername",
            email="test@test.com",
            first_name="Jane",
            last_name="Smith",
            password="tester!123"
        )
        self.user.save()

        self.blog = Blog.objects.create(
            title="4 Resorts Bora Bora",
            slug="4-resorts-bora-bora",
            author=self.user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog.save()

        self.blog2 = Blog.objects.create(
            title="Resort Blog",
            slug="resort-blog",
            author=self.user,
            content="this is test content",
            blog_img="test.jpg"
        )
        self.blog2.save()

    def test_blog_creation(self):
        """
        Test model for the Blog creation.
        """
        self.assertIsInstance(self.blog, Blog)
        self.assertTrue(Blog.objects.exists())

    def test_blog_fields_valid(self):
        """
        Test all Blog fields are valid.
        """
        self.assertEqual(self.blog.title, "4 Resorts Bora Bora")
        self.assertEqual(self.blog.slug, "4-resorts-bora-bora")
        self.assertEqual(self.blog.author, self.user)
        self.assertEqual(self.blog.content, "this is test content")
        self.assertTrue(self.blog.created)
        self.assertTrue(self.blog.updated)
        self.assertEqual(self.blog.status, 1)
        self.assertEqual(self.blog.featured, False)
        self.assertEqual(self.blog.blog_img, "test.jpg")

    def test_blog_user_favorited(self):
        """
        Test for when a user favorites a blog.
        """
        blog = Blog.objects.get(id=1)
        blog.favorite.add(self.user)
        blog.save()
        self.assertTrue(blog.favorite)

    def test_blog_default_fields(self):
        """
        Test for Blog default values upon creation.
        """
        self.assertEqual(self.blog2.status, 0)
        self.assertEqual(self.blog2.featured, False)

    def test_blog_str_method(self):
        """
        Test Blog __str__() method returns title.
        """
        self.assertEqual(str(self.blog.title), '4 Resorts Bora Bora')


class BlogCommentModelTest(TestCase):
    def setUp(self):
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

        self.user3 = User.objects.create(
            username="test",
            email="test@t.com",
            first_name="Jane",
            last_name="Smith",
            password="tester!123"
        )
        self.user3.save()

        self.blog = Blog.objects.create(
            title="4 Resorts Bora Bora",
            slug="4-resorts-bora-bora",
            author=self.user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog.save()

        self.blog_comment = BlogComment.objects.create(
            user=self.user,
            blog=self.blog,
            comment="this is a comment",
        )
        self.blog_comment.likes.add(self.user)
        self.blog_comment.save()

        self.blog_comment2 = BlogComment.objects.create(
            user=self.user2,
            blog=self.blog,
            comment="this is a comment",
        )
        self.blog_comment2.save()

    def test_blog_comment_creation(self):
        """
        Test model for Blog Comment creation.
        """
        self.assertIsInstance(self.blog_comment, BlogComment)
        self.assertTrue(BlogComment.objects.get(Q(user=self.user) & Q(blog=self.blog)))
        self.assertTrue(BlogComment.objects.exists())

    def test_blog_comment_valid(self):
        """
        Test all BlogComment fields for validity.
        """
        self.assertEqual(self.blog_comment.user, self.user)
        self.assertEqual(self.blog_comment.blog, self.blog)
        self.assertEqual(self.blog_comment.comment, "this is a comment")
        self.assertEqual(self.blog_comment.likes.filter(id=self.user.id).count(), 1)
        self.assertTrue(self.blog_comment.created)
        self.assertFalse(self.blog_comment.updated)

    def test_blog_comment_like_remove(self):
        """
        Test that user can remove their like from blog comment.
        """
        self.blog_comment.likes.remove(self.user)
        self.assertNotIn(self.user, self.blog_comment.likes.all())

    def test_blog_comment_like_add(self):
        """
        Test that user can add their like to blog comment.
        """
        self.blog_comment.likes.add(self.user)
        self.assertIn(self.user, self.blog_comment.likes.all())

    def test_blog_commented_has_user_comment_true(self):
        """
        Test has_user_commented() method returns True.
        """
        comment = BlogComment.has_user_commented(self.user.id, self.blog.id)
        self.assertTrue(comment)

    def test_blog_commented_has_user_comment_false(self):
        """
        Test has_user_commented() method returns False.
        """
        comment = BlogComment.has_user_commented(self.user3.id, self.blog.id)
        self.assertFalse(comment)
