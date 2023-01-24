from django.db import models


class Contact(models.Model):
    """
    Model for storing Contact data.
    """
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contacts"
        ordering = ('created',)
    
    def __str__(self):
        return self.email
        