from django import forms
from blog.models import BlogComment


class UserCommentForm(forms.ModelForm):
    """
    Form used when Users comment on a blog post.
    """
    comment = forms.Textarea()

    class Meta:
        model = BlogComment
        fields = [
            'comment'
        ]
