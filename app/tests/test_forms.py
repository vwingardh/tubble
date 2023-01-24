from django.test import TestCase
from app.forms import ContactForm


class ContactFormTest(TestCase):
    def test_contact_form_all_valid(self):
        """
        Test if all form data is valid.
        """
        form_data={
            'first_name': 'Jane', 
            'last_name': 'Smith',
            'email': 'test@test.com',
            'message': 'this is a test'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_missing_first_name(self):
        """
        Test form for missing required first name.
        """
        form_data={ 
            'last_name': 'Smith',
            'email': 'test@test.com',
            'message': 'this is a test'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_contact_form_missing_last_name(self):
        """
        Test form for missing required last name.
        """
        form_data={ 
            'first_name': 'Jane',
            'email': 'test@test.com',
            'message': 'this is a test'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_contact_form_missing_email(self):
        """
        Test form for missing required email.
        """
        form_data={ 
            'first_name': 'Jane',
            'last_name': 'Smith',
            'message': 'this is a test'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_contact_form_missing_message(self):
        """
        Test form for missing required message.
        """
        form_data={ 
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'test@test.com'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
        