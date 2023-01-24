from django.test import TestCase
from account.forms import RegisterUserForm, UserProfileForm


class RegisterUserFormTest(TestCase):
    """
    Test form validation for all fields.
    """
    def test_register_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'first_name': 'Jane', 
            'last_name': 'Smith',
            'password1': 'tester!123',
            'password2': 'tester!123'
        }
        form = RegisterUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_missing_username(self):
        """
        Test if the form raises an error when username is missing.
        """
        form_data = {
            'email': 'test@test.com',
            'first_name': 'Jane', 
            'last_name': 'Smith',
            'password1': 'tester!123',
            'password2': 'tester!123'
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_register_form_missing_email(self):
        """
        Test if the form raises an error when email is missing.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Jane', 
            'last_name': 'Smith',
            'password1': 'tester!123',
            'password2': 'tester!123'
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_register_form_missing_first_name(self):
        """
        Test if the form raises an error when first name is missing.
        """
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com', 
            'last_name': 'Smith',
            'password1': 'tester!123',
            'password2': 'tester!123'
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_register_form_missing_last_name(self):
        """
        Test if the form raises an error when last name is missing.
        """
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com', 
            'first_name': 'Jane',
            'password1': 'tester!123',
            'password2': 'tester!123'
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_register_form_missing_password1(self):
        """
        Test if the form raises an error when password1 is missing.
        """
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com', 
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password2': 'tester!123'
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_register_form_missing_password2(self):
        """
        Test if the form raises an error when password2 is missing.
        """
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com', 
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password1': 'tester!123'
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_register_form_password_match_method_false(self):
        """
        Test RegisterUserForm is_password_match() method returns False.
        """
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'first_name': 'Jane', 
            'last_name': 'Smith',
            'password1': 'tester',
            'password2': 'tester!123'
        }
        same_password = RegisterUserForm.is_password_match(
            form_data['password1'], form_data['password2']
        )
        self.assertFalse(same_password)

    def test_register_form_password_match_method_true(self):
        """
        Test RegisterUserForm is_password_match() method returns True.
        """
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'first_name': 'Jane', 
            'last_name': 'Smith',
            'password1': 'tester!123',
            'password2': 'tester!123'
        }
        same_password = RegisterUserForm.is_password_match(
            form_data['password1'], form_data['password2']
        )
        self.assertTrue(same_password)

    
class UserProfileFormTest(TestCase):
    """
    Test form validation for all fields.
    """
    def test_user_profile_form_valid(self):
        form_data = {
            'bio': 'This is a test',
            'age': 30,
            'gender': 'woman',
            'location': 'Stockholm',
            'profile_img': 'test.jpg',
            'countries_visited': ['SE']
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_no_data(self):
        """
        Test form validation for optional form fields.
        """
        form_data = {}
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
