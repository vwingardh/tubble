from django.test import TestCase
from app.models import Contact


class ContactModelTest(TestCase):
    """
    Test setup for Contact model.
    """
    def setUp(self):
        self.contact = Contact.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='test@test.com',
            message='this is a test'
        )
        self.contact.save()

    def test_contact_creation(self):
        """
        Test model for the Contact creation.
        """
        self.assertIsInstance(self.contact, Contact)
        self.assertTrue(Contact.objects.exists())

    def test_contact_fields(self):
        """
        Test all Contact object fields.
        """
        self.assertEqual(self.contact.first_name, 'Jane')
        self.assertEqual(self.contact.last_name, 'Smith')
        self.assertEqual(self.contact.email, 'test@test.com')
        self.assertEqual(self.contact.message, 'this is a test')
        self.assertIsNotNone(self.contact.created)

    def test_str_method(self):
        """
        Test Contact __str__() method returns email.
        """
        self.assertEqual(str(self.contact.email), 'test@test.com')
