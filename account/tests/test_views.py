from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from workspace.models import Destination
from blog.models import Blog
from account.models import UserProfile
from django.contrib.auth.models import AnonymousUser
from account.forms import UserProfileForm


class UserProfileViewTest(TestCase):
    """
    Test setup for Request, User, Destinations, and 3 blog posts.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="testusername",
            email="test@test.com",
            first_name="Jane",
            last_name="Smith",
            password="tester!123"
        )
        self.user.save()

        self.destination = Destination.objects.create(
            user=self.user,
            city="testcity",
            country="testcountry",
            slug="testcity",
            adventure_type="Beach and ocean",
            climate="Tropical",
            flight="Quick",
            has_user_visited=False
        )
        self.destination.save()

        self.destination_visited = Destination.objects.create(
            user=self.user,
            city="testcityvisited",
            country="testcountry",
            slug="testcity",
            adventure_type="Beach and ocean",
            climate="Tropical",
            flight="Quick",
            has_user_visited=True
        )
        self.destination_visited.save()

        user = User.objects.get(id=1)
        self.blog1 = Blog.objects.create(
            title="4 Resorts Bora Bora",
            slug="4-resorts-bora-bora",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog1.favorite.add(user)
        self.blog1.save()

        self.blog2 = Blog.objects.create(
            title="Top Places to See in Rome",
            slug="top-places-to-see-in-rome",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog2.favorite.add(user)
        self.blog2.save()

        self.blog3 = Blog.objects.create(
            title="5 Reasons to Visit Yellowstone",
            slug="5-reasons-to-visit-yellowstone",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog3.favorite.add(user)
        self.blog3.save()

    def test_profile_creation(self):
        """
        Test User, Destination, and Blog creation.
        """
        self.assertIsInstance(self.user, User)
        self.assertTrue(Destination.objects.exists())
        self.assertTrue(Blog.objects.exists())

    def test_user_view_profile(self):
        """
        Test user_view_profile() view function with authenticated user.
        """
        user = self.user
        self.client.force_login(user)
        response = self.client.get(reverse('account:user_view_profile', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/public-user-profile.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['total_destinations_created'], 1)
        self.assertEqual(response.context['total_visited_destinations_created'], 1)

    def test_user_view_profile_non_authenticated(self):
        """
        Test user_view_profile() @login_required decorator 
        """
        user = AnonymousUser()
        response = self.client.get('account/user_view_profile/', kwargs={'username': user.username})
        self.assertEqual(response.status_code, 404)


class UserRegistrationViewTest(TestCase):
    """
    Test setup for Request
    """
    def setUp(self):
        self.client = Client()

    def test_user_registration_POST(self):
        """
        Test user_registration() view function creating a new user.
        """
        form_data = {
            'username':'tester',
            'email':'test@test.com',
            'first_name':'Jane',
            'last_name':'Smith',
            'password1':'tester!123',
            'password2':'tester!123'
        }
        response = self.client.post(reverse('account:user_registration'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form_data['username'], 'tester')

    def test_user_registration_GET(self):
        """
        Test user_registration() view function viewing RegisterUserForm - no data
        """
        response = self.client.get(reverse('account:user_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')


class UserRegistrationViewTest(TestCase):
    """
    Test setup for Request, User, UserProfile, and 3 blog posts.
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('account:user_update_profile')
        self.user = User.objects.create(
            username="testusername",
            email="test@test.com",
            first_name="Jane",
            last_name="Smith",
            password="tester!123"
        )
        self.user.save()
        self.user_profile = UserProfile.get_user_profile(self.user)
        self.countries_visited = UserProfile.get_country_list(self.user)

        user = User.objects.get(id=1)
        self.blog1 = Blog.objects.create(
            title="4 Resorts Bora Bora",
            slug="4-resorts-bora-bora",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog1.favorite.add(user)
        self.blog1.save()

        self.blog2 = Blog.objects.create(
            title="Top Places to See in Rome",
            slug="top-places-to-see-in-rome",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog2.favorite.add(user)
        self.blog2.save()

        self.blog3 = Blog.objects.create(
            title="5 Reasons to Visit Yellowstone",
            slug="5-reasons-to-visit-yellowstone",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog3.favorite.add(user)
        self.blog3.save()

        self.profile = UserProfile.objects.create(
            user=user,
            bio='This is a test',
            age=30,
            gender='woman',
            location='Stockholm',
            profile_img='test.jpg'
        )
        self.profile.save()

    def test_user_update_profile_GET_non_authenticated(self):
        """
        Test user_update_profile() view function GET template 
        non-authenticated user.
        """
        user = AnonymousUser()
        response = self.client.get(reverse('account:user_update_profile'))
        self.assertEqual(response.status_code, 302)

    def test_user_update_profile_GET_authenticated(self):
        """
        Test user_update_profile() view function GET template
        authenticated user.
        """
        user = self.user
        self.client.force_login(user)
        response = self.client.get(reverse('account:user_update_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/update-profile.html')

    def test_user_update_profile_GET_existing_form_data(self):
        """
        Test user_update_profile() view function with existing user form data.
        """
        user = self.user
        self.client.force_login(user)
        self.user_profile = True
        profile = UserProfile.objects.get(user=user.id)
        self.form_data = UserProfileForm(instance=profile)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_user_update_profile_initial_POST(self):
        """
        Test user_update_profile() view function POST initial form data on first login.
        """
        user = self.user
        self.client.force_login(user)
        self.user_profile = False
        self.form_data = {
            'bio': 'This is a test',
            'age': 30,
            'gender': 'woman',
            'location': 'Stockholm',
            'profile_img': 'test.jpg'
        }
        response = self.client.post(reverse('account:user_update_profile'), self.form_data)
        self.assertEqual(response.status_code, 302)
        profile = UserProfile.objects.get(user_id=1)
        self.assertEqual(profile.age, 30)
        
    def test_user_update_profile_updated_POST(self):
        """
        Test user_update_profile() view function POST updated form data.
        """
        user = self.user
        self.client.force_login(user)
        self.user_profile = True
        profile = UserProfile.objects.get(user=user.id)
        form_data = UserProfileForm(instance=profile)
        response = self.client.post(reverse('account:user_update_profile'))
        self.assertEqual(response.status_code, 302)
