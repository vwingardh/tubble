from django.test import TestCase
from blog.forms import UserCommentForm


class UserCommentFormTest(TestCase):
    def test_user_comment_form_valid(self):
        """
        Test if all form data is valid.
        """
        form_data={
            'comment': 'This is a test'
        }
        form = UserCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_comment_form_missing_comment(self):
        """
        Test form with missing comment.
        """
        form_data={
            'comment': 'This is a test'
        }
        form = UserCommentForm(data=form_data)
        self.assertTrue(form.is_valid())
