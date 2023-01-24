from django.db import models
from django.conf import settings
from django.db.models import Q


class Destination(models.Model):
    """
    Destination model for bucket list destinations and 
    visited destinations.
    """
    class DestinationObjects(models.Manager):
        """
        Manager returns Destination objects that have not been visited
        by user - user has not been to that specific country.
        """
        def get_queryset(self):
            return super().get_queryset().filter(has_user_visited=False)

    class VisitedObjects(models.Manager):
        """
        Manager returns Destination objects that have been visited
        by user - user has been to that specific country.
        """
        def get_queryset(self):
            return super().get_queryset().filter(has_user_visited=True)    

    ADVENTURE_TYPE = (
        ('Beach and ocean', 'Beach and ocean'),
        ('City attractions', 'City attractions'),
        ('Sport event', 'Sport event'),
        ('Outdoor activities', 'Outdoor activities'),
        ('Food and restaurants', 'Food and restaurants'),
        ('Historical landmarks', 'Historical landmarks')
    )
    CLIMATE = (
        ('Tropical', 'Tropical'),
        ('Subtropical', 'Subtropical'),
        ('Temperate', 'Temperate'),
        ('Desert', 'Desert'),
        ('Mediterranean', 'Mediterranean'),
        ('Highlands', 'Highlands'),
        ('Polar', 'Polar')
    )
    FLIGHT = (
        ('Quick', 'Quick'),
        ('Short', 'Short'),
        ('Medium', 'Medium'),
        ('Long', 'Long'),
        ('Very long', 'Very long')

    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="destinations"
    )
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    adventure_type = models.CharField(
        choices=ADVENTURE_TYPE, 
        max_length=50
    )
    climate = models.CharField(choices=CLIMATE, max_length=50)
    flight = models.CharField(choices=FLIGHT, max_length=50)
    notes = models.TextField(blank=True)
    activity1 = models.TextField(blank=True)
    activity2 = models.TextField(blank=True)
    activity3 = models.TextField(blank=True)
    activity4 = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='user_destination_images/', 
        blank=True, 
        default='user_destination_images/default.png'
    )
    created = models.DateTimeField(auto_now_add=True)
    has_user_visited = models.BooleanField(
        null=True, 
        blank=True, 
        default=False
    )
    # default manager
    objects = models.Manager()
    # has_user_visited == False custom manager
    destination_objects = DestinationObjects() 
    # has_user_visited == True custom manager
    visited_destination_objects = VisitedObjects() 

    class Meta:
        verbose_name_plural = "Destinations"
        ordering = ('city',)

    def __str__(self):
        return self.city

    def save(self, *args, **kwargs):
        """
        Method ensures city, country, and 
        slug are saved in lower case.
        """
        self.city = self.city.lower()
        self.country = self.country.lower()
        self.slug = self.slug.lower()
        return super(Destination, self).save(*args, **kwargs)

    def get_choices_list(choice_field):
        """
        Method returns a list of filter choices made by user.
        """
        choices = Destination._meta.get_field(choice_field).choices
        choices_list = []
        for i in choices:
            choices_list.append(i[1])
        return choices_list

    def get_destination_exists(city, country, user_id):
        """
        Method prevents user from creating duplicate destination.
        """
        try:
            destination = Destination.destination_objects.get(
                Q(city=city) & Q(country=country) & Q(user_id=user_id)
            )
            if destination:
                return True
        except:
            return False
    
    def get_visited_destination_exists(city, country, user_id):
        """
        Method prevents user from creating a visited destination
        if the destination has already been created 
        under 'visited destinations'.
        """
        try:
            destination = Destination.visited_destination_objects.get(
                Q(city=city) & Q(country=country) & Q(user_id=user_id)
            )
            if destination:
                return True
        except:
            return False
    