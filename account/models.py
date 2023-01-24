from django_countries.fields import CountryField

from django.db import models
from django.contrib.auth.models import User

    
class UserProfile(models.Model):
    """
    UserProfile model stores user information
    """
    GENDER = (
        ('woman', 'woman'),
        ('man', 'man'),
        ('traveler', 'traveler'),
        ('transgender woman', 'transgender woman'),
        ('transgender man', 'transgender man'),
        ('non-binary', 'non-binary'),
        ('agender', 'agender')
    )
    
    ADVENTURE_LEVEL = (
        ('Travel Enthusiast', 'Travel Enthusiast'),
        ('Adventurer', 'Adventurer'),
        ('Globetrotter', 'Globetrotter')
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name="user_profile"
    )
    bio = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDER, blank=True, null=True, max_length=150)
    location = models.CharField(max_length=150, blank=True, null=True)
    profile_img = models.ImageField(
        upload_to='user_profile_images/',
        blank=True, 
        default='user_profile_images/default-user-image.png'
    )
    countries_visited = CountryField(multiple=True, blank=True)
    adventure_level = models.CharField(
        choices=ADVENTURE_LEVEL, 
        default='Travel Enthusiast', 
        max_length=150
    )

    def __str__(self):
        return self.user.username

    def get_user_profile(user):
        """
        Method returns True or False if user exists. Used to 
        determine if a user is creating a UserProfile or
        updating their UserProfile.
        """
        try:
            user_profile = UserProfile.objects.get(user=user.id)
            if user_profile:
                return True
        except:
            return False

    def set_adventure_level(user):
        """
        Method sets a user's adventure level status based on
        how many countries the user has visited.
        """
        user_profile = UserProfile.objects.get(user=user)
        country_count = len(user_profile.countries_visited)
        if country_count <= 4:
            user_profile.adventure_level = 'Travel Enthusiast'
        elif country_count >= 5 and country_count <= 9:
            user_profile.adventure_level = 'Adventurer'
        else:
            user_profile.adventure_level = 'Globetrotter' 
        user_profile.save()
        


    def get_country_list(user):
        """
        Method returns a list of only country names if user exists, 
        otherwise returns an empty list.
        """
        try:
            user_profile = UserProfile.objects.get(user=user.id)
            countries_visited_list = []
            for c in user_profile.countries_visited:
                country = str(c)
                countries_visited_list.append(country)
            return countries_visited_list
        except:
            return []
