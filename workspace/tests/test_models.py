from django.test import TestCase
from workspace.models import Destination
from django.contrib.auth.models import User


class DestinationModelTest(TestCase):
    """
    Test setup for testing Destination model.
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

        self.destination = Destination.objects.create(
            user=self.user,
            city="Testcity",
            country="Testcountry",
            slug="Testcity",
            adventure_type="Beach and ocean",
            climate="Tropical",
            flight="Quick",
            notes="test notes",
            activity1="test1",
            activity2="test2",
            activity3="test3",
            activity4="test4"
        )
        self.destination.save()

    def test_destination_creation(self):
        """
        Test User and Destination object creation.
        """
        self.assertIsInstance(self.destination, Destination)
        self.assertTrue(Destination.objects.exists())

    def test_destination_fields(self):
        """
        Test Destination fields.
        """
        self.assertEqual(self.destination.user, self.user)
        self.assertEqual(self.destination.city, 'testcity')
        self.assertEqual(self.destination.country, 'testcountry')
        self.assertEqual(self.destination.slug, 'testcity')
        self.assertEqual(self.destination.adventure_type, 'Beach and ocean')
        self.assertEqual(self.destination.climate, 'Tropical')
        self.assertEqual(self.destination.flight, 'Quick')
        self.assertEqual(self.destination.notes, 'test notes')
        self.assertEqual(self.destination.activity1, 'test1')
        self.assertEqual(self.destination.activity2, 'test2')
        self.assertEqual(self.destination.activity3, 'test3')
        self.assertEqual(self.destination.activity4, 'test4')
        self.assertEqual(self.destination.image, 'user_destination_images/default.png')
        self.assertTrue(self.destination.created)
        self.assertEqual(self.destination.has_user_visited, False)

    def test_str_method(self):
        """
        Test Destination __str__() method returns city.
        """
        self.assertEqual(str(self.destination.city), 'testcity')

    def test_save(self):
        """
        Test Destination save() method saves lower case city, country, slug.
        """
        self.assertTrue(self.destination.city == 'testcity')
        self.assertTrue(self.destination.country == 'testcountry')
        self.assertTrue(self.destination.slug == 'testcity')

    def get_choices_list(self):
        """
        Test Destination get_choices_list() method 
        returns list of choices.
        """
        self.assertEqual(
            Destination.get_choices_list(
                choice_field='adventure_type'
                ), ['Beach and ocean']
            )
        self.assertEqual(
            Destination.get_choices_list(
                choice_field='climate'
                ), ['Tropical']
            )
        self.assertEqual(
            Destination.get_choices_list(
                choice_field='flight'
                ), ['Quick']
            )

    def get_destination_exists_true(self):
        """
        Test Destination get_destination_exists() method 
        returns True.
        """
        self.assertTrue(
            Destination.get_destination_exists(
                self.destination.city, self.destination.country
            )
        )
        
    def get_destination_exists_false(self):
        """
        Test Destination get_destination_exists() method 
        returns False.
        """
        self.assertFalse(
            Destination.get_destination_exists(
                'stockholm', 
                'sweden'
            )
        )
