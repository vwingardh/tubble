from django.test import TestCase
from workspace.forms import DestinationCreateForm, NextAdventureFilterForm


class TestDestinationCreateForm(TestCase):
    def test_destination_create_form_valid(self):
        """
        Test if all form data is valid.
        """
        form_data = {
            'user': 1,
            'city': 'test-city',
            'country': 'test-country',
            'adventure_type': 'Beach and ocean',
            'climate': 'Tropical',
            'flight': 'Quick',
            'notes': 'this is notes',
            'activity1': 'test1',
            'activity2': 'test2',
            'activity3': 'test3',
            'activity4': 'test4',
            'image': 'test.jpg',
            'has_user_visited': False,
        }
        form = DestinationCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_destination_create_form_missing_city(self):
        """
        Test form validation for missing city.
        """
        form_data = {
            'user': 1,
            'country': 'test-country',
            'adventure_type': 'Beach and ocean',
            'climate': 'Tropical',
            'flight': 'Quick',
            'notes': 'this is notes',
            'activity1': 'test1',
            'activity2': 'test2',
            'activity3': 'test3',
            'activity4': 'test4',
            'image': 'test.jpg',
            'has_user_visited': False,
        }
        form = DestinationCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('city', form.errors)

    def test_destination_create_form_missing_country(self):
        """
        Test form validation for missing country.
        """
        form_data = {
            'user': 1,
            'city': 'test-city',
            'adventure_type': 'Beach and ocean',
            'climate': 'Tropical',
            'flight': 'Quick',
            'notes': 'this is notes',
            'activity1': 'test1',
            'activity2': 'test2',
            'activity3': 'test3',
            'activity4': 'test4',
            'image': 'test.jpg',
            'has_user_visited': False,
        }
        form = DestinationCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors)

    def test_destination_create_form_missing_adventure_type(self):
        """
        Test form validation for missing adventure type.
        """
        form_data = {
            'user': 1,
            'city': 'test-city',
            'country': 'test-country',
            'climate': 'Tropical',
            'flight': 'Quick',
            'notes': 'this is notes',
            'activity1': 'test1',
            'activity2': 'test2',
            'activity3': 'test3',
            'activity4': 'test4',
            'image': 'test.jpg',
            'has_user_visited': False,
        }
        form = DestinationCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('adventure_type', form.errors)

    def test_destination_create_form_missing_climate(self):
        """
        Test form validation for missing climate.
        """
        form_data = {
            'user': 1,
            'city': 'test-city',
            'country': 'test-country',
            'adventure_type': 'Beach and ocean',
            'flight': 'Quick',
            'notes': 'this is notes',
            'activity1': 'test1',
            'activity2': 'test2',
            'activity3': 'test3',
            'activity4': 'test4',
            'image': 'test.jpg',
            'has_user_visited': False,
        }
        form = DestinationCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('climate', form.errors)

    def test_destination_create_form_missing_flight(self):
        """
        Test form validation for missing flight.
        """
        form_data = {
            'user': 1,
            'city': 'test-city',
            'country': 'test-country',
            'adventure_type': 'Beach and ocean',
            'climate': 'Tropical',
            'notes': 'this is notes',
            'activity1': 'test1',
            'activity2': 'test2',
            'activity3': 'test3',
            'activity4': 'test4',
            'image': 'test.jpg',
            'has_user_visited': False,
        }
        form = DestinationCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('flight', form.errors)

    def test_destination_create_form_optional(self):
        """
        Test form validation for optional fields.
        """
        form_data = {
            'city': 'test-city',
            'country': 'test-country',
            'adventure_type': 'Beach and ocean',
            'climate': 'Tropical',
            'flight': 'Quick',
        }
        form = DestinationCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_destination_create_form_default_fields(self):
        """
        Test form for default fields.
        """
        form_data = {
            'city': 'test-city',
            'country': 'test-country',
            'adventure_type': 'Beach and ocean',
            'climate': 'Tropical',
            'flight': 'Quick',
        }
        form = DestinationCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form['has_user_visited'].initial == False)
        

class TestNextAdventureFilterForm(TestCase):
    """
    Test form validation for all fields.
    """
    def test_next_adventure_filter_form_valid(self):
        form_data = {
            'adventure': 'Beach and ocean',
            'climate': 'Tropical',
            'flight': 'Quick'
        }
        form = NextAdventureFilterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_next_adventure_filter_missing_adventure(self):
        """
        Test if the form raises an error when adventure is missing.
        """
        form_data = {
            'climate': 'Tropical',
            'flight': 'Quick'
        }
        form = NextAdventureFilterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('adventure', form.errors)

    def test_next_adventure_filter_missing_climate(self):
        """
        Test if the form raises an error when climate is missing.
        """
        form_data = {
            'adventure': 'Beach and ocean',
            'flight': 'Quick'
        }
        form = NextAdventureFilterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('climate', form.errors)

    def test_next_adventure_filter_missing_flight(self):
        """
        Test if the form raises an error when flight is missing.
        """
        form_data = {
            'adventure': 'Beach and ocean',
            'climate': 'Tropical'
        }
        form = NextAdventureFilterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('flight', form.errors)
