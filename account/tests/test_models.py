from django.test import TestCase
from account.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser


class UserProfileModelTest(TestCase):
    """
    Test setup for User and User Profile.
    """
    def setUp(self):
        self.user = User.objects.create(
            username="testusername",
            email="test@test.com",
            first_name="Jane",
            last_name="Smith",
            password="tester!123"
        )
        self.user.save()

        self.user_profile = UserProfile.objects.create(
            user=self.user,
            bio="This is a test", 
            age="30",
            gender="woman",
            location="Stockholm",
            countries_visited=['SE'],
            adventure_level="Travel Enthusiast"
        )
        self.user_profile.save()

    def test_profile_creation(self):
        """
        Test User and User Profile creation.
        """
        self.assertIsInstance(self.user_profile, UserProfile)
        self.assertTrue(UserProfile.objects.exists())

    def test_profile_fields(self):
        """
        Test User Profile fields.
        """
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.bio, 'This is a test')
        self.assertEqual(self.user_profile.age, '30')
        self.assertEqual(self.user_profile.gender, 'woman')
        self.assertEqual(self.user_profile.location, 'Stockholm')
        self.assertEqual(self.user_profile.profile_img.url, '/media/user_profile_images/default-user-image.png')
        self.assertEqual(self.user_profile.countries_visited, ['SE'])
        self.assertEqual(self.user_profile.adventure_level, 'Travel Enthusiast')

    def test_str_method(self):
        """
        Test User Profile __str__() method returns username.
        """
        self.assertEqual(str(self.user_profile.user.username), 'testusername')

    def test_get_user_profile_True(self):
        """
        Test User Profile get_user_profile() method returns True.
        """
        self.assertTrue(UserProfile.get_user_profile(user=self.user))

    def test_get_user_profile_False(self):
        """
        Test User Profile get_user_profile() method returns False.
        """
        user = AnonymousUser()
        self.assertFalse(UserProfile.get_user_profile(user=user))

    def test_set_adventure_level_travel_enthusiast(self):
        """
        Test User Profile set_adventure_level() method sets 'Travel Enthusiast'.
        """
        adventure_level = UserProfile.set_adventure_level(user=self.user)
        user_profile = UserProfile.objects.get(user=self.user.id)
        self.assertEqual(user_profile.adventure_level, 'Travel Enthusiast')

    def test_set_adventure_level_adventurer(self):
        """
        Test User Profile set_adventure_level() method sets 'Adventurer'.
        """
        set_countries = UserProfile.objects.get(user=self.user.id)
        set_countries.countries_visited = ['US', 'FI', 'JP', 'AU', 'DE', 'SE']
        set_countries.save()
        adventure_level = UserProfile.set_adventure_level(user=self.user)
        user_profile = UserProfile.objects.get(user=self.user.id)
        self.assertEqual(user_profile.adventure_level, 'Adventurer')

    def test_set_adventure_level_globetrotter(self):
        """
        Test User Profile set_adventure_level() method sets 'Globetrotter'.
        """
        set_countries = UserProfile.objects.get(user=self.user.id)
        set_countries.countries_visited = [
            'US', 'FI', 'JP', 'AU', 'DE', 'SE', 'ES', 'GB', 'TH', 'KZ'
        ]
        set_countries.save()
        adventure_level = UserProfile.set_adventure_level(user=self.user)
        user_profile = UserProfile.objects.get(user=self.user.id)
        self.assertEqual(user_profile.adventure_level, 'Globetrotter')

    def test_get_country_list(self):
        """
        Test User Profile get_country_list() method returns list of country names only.
        """
        country_list = UserProfile.get_country_list(user=self.user)
        self.assertListEqual(country_list, ["SE"])

    def test_get_country_list_no_countries(self):
        """
        Test User Profile get_country_list() method returns empty list.
        """
        user = AnonymousUser()
        country_list = UserProfile.get_country_list(user=user)
        self.assertListEqual(country_list, [])
