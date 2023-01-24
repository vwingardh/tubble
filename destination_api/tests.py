from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth.models import User
from workspace.models import Destination


class DestinationAPITest(APITestCase):
    """
    Testing for Tubble API's
    """
    def setUp(self):
        self.url_destination_list = reverse('api:destination_list')
        self.url_count_list = reverse('api:destination_count')
        self.url_city_activity_list = reverse('api:destination_activity_list')
        self.user = User.objects.create_user(
            username='testusername',
            password='tester!123'
        )

        self.destination1 = Destination.objects.create(
            user=self.user,
            city='stockholm',
            country='sweden',
            slug='stockholm',
            adventure_type='beach and ocean',
            climate='tropical',
            flight='2 hours or less',
            notes='testing notes',
        )
        self.destination1.save()

        self.destination2 = Destination.objects.create(
            user=self.user,
            city='copenhagen',
            country='denmark',
            slug='denmark',
            adventure_type='beach and ocean',
            climate='tropical',
            flight='2 hours or less',
            activity1='test place',
            notes='testing notes',
        )
        self.destination2.save()

    def test_destination_list_api_non_authenticated(self):
        """
        Test that non-authenticated users cannot access API.
        """
        response = self.client.get(self.url_destination_list)
        self.assertEqual(response.status_code, 403)

    def test_destination_list_api_authenticated(self):
        """
        Test that authenticated users can access API.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url_destination_list)
        self.assertEqual(response.status_code, 200)

    def test_destination_list_api_GET(self):
        """
        Test API returns city and country 
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url_destination_list)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['city'], 'copenhagen')
        self.assertEqual(response.data[0]['country'], 'denmark')
        self.assertEqual(response.data[1]['city'], 'stockholm')
        self.assertEqual(response.data[1]['country'], 'sweden')

    def test_destination_city_count_list_api_non_authenticated(self):
        """
        Test that non-authenticated users cannot access API.
        """
        response = self.client.get(self.url_count_list)
        self.assertEqual(response.status_code, 403)

    def test_destination_city_count_list_api_authenticated(self):
        """
        Test that authenticated users can access API.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url_count_list)
        self.assertEqual(response.status_code, 200)

    def test_destination_city_count_list_api_GET(self):
        """
        Test API returns city and count.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url_count_list)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['city'], 'stockholm')
        self.assertEqual(response.data[0]['count'], 1)
        self.assertEqual(response.data[1]['city'], 'copenhagen')
        self.assertEqual(response.data[1]['count'], 1)

    def test_destination_city_activity_list_api_non_authenticated(self):
        """
        Test that non-authenticated users cannot access API.
        """
        response = self.client.get(self.url_city_activity_list)
        self.assertEqual(response.status_code, 403)

    def test_destination_city_activity_list_api_authenticated(self):
        """
        Test that authenticated users cannot access API.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url_city_activity_list)
        self.assertEqual(response.status_code, 200)

    def test_destination_city_activity_list_api_GET(self):
        """
        Test API returns a city and its associated activities.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url_city_activity_list)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['city'], 'copenhagen')
        self.assertEqual(response.data[0]['activity1'], 'test place')
