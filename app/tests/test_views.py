from django.urls import reverse
from django.test import TestCase, Client
from app.models import Contact
from blog.models import Blog
from workspace.models import Destination
from django.contrib.auth.models import User


class ContactViewTest(TestCase):
    """
    Test setup for contact view.
    """
    def setUp(self):
        self.client=Client()
        self.url=reverse('app:contact')
        self.contact = Contact.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='test@test.com',
            message='this is a test'
        )
        self.contact.save()

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

    def test_contact_creation(self):
        """
        Test Contact creation.
        """
        self.assertIsInstance(self.contact, Contact)
        self.assertTrue(Contact.objects.exists())

    def test_contact_GET(self):
        """
        Test contact() view get template.
        """
        response = self.client.get(reverse('app:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/resources/contact-us.html')

    def test_contact_POST(self):
        """
        Test contact() view post form data.
        """
        self.form_data={
            'first_name': 'jane',
            'last_name': 'smith',
            'email': 'test@t.com',
            'message': 'test message'
        }
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)
        contact = Contact.objects.get(id=2)
        self.assertEqual(contact.first_name, 'jane')
        self.assertEqual(contact.last_name, 'smith')
        self.assertEqual(contact.email, 'test@t.com')
        self.assertEqual(contact.message, 'test message')

    def test_contact_POST_missing_first_name(self):
        """
        Test contact() view post form data with missing first name.
        """
        self.form_data={
            'last_name': 'smith',
            'email': 'test@t.com',
            'message': 'test message'
        }
        response = self.client.post(reverse('app:contact'))
        self.assertIn('This field is required.', response.context['errors'])
        self.assertEqual(response.status_code, 200)

    def test_index_no_destinations(self):
        """
        Test index() view with no destinations.
        """
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/index.html')

    def test_index_destinations(self):
        """
        Test index() view with destinations.
        """
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/index.html')
        self.assertTrue(response.context['destinations'])

    def test_features_view(self):
        """
        Test features() view.
        """
        response = self.client.get(reverse('app:features'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/resources/features.html')

    def test_pricing_view(self):
        """
        Test pricing() view.
        """
        response = self.client.get(reverse('app:pricing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/resources/pricing.html')

    def test_preview_view(self):
        """
        Test preview() view.
        """
        response = self.client.get(reverse('app:preview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/resources/preview.html')

    def test_about_tubble_view(self):
        """
        Test abbout_tubble() view.
        """
        response = self.client.get(reverse('app:about_tubble'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/resources/about-us.html')

    def test_careers_view(self):
        """
        Test careers() view.
        """
        response = self.client.get(reverse('app:careers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/resources/careers.html')

    def test_mobile_app_view(self):
        """
        Test mobile_app() view.
        """
        response = self.client.get(reverse('app:mobile_app'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/resources/mobile-app.html')
        