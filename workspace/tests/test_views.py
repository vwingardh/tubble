from django.urls import reverse
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from blog.models import Blog
from workspace.models import Destination
from workspace.views import (
    workspace_home,
    filter_next_adventure,
    create_destination,
    destination_detail_view,
    update_destination,
    delete_destination
)


class TestWorkspaceViews(TestCase):
    """
    Test setup for testing workspace view functions.
    """
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username="testusername",
            email="test@test.com",
            first_name="Jane",
            last_name="Smith",
            password="tester!123"
        )
        self.user.save()

        self.destination = Destination.objects.create(
            user=self.user,
            city="testcity",
            country="testcountry",
            slug="testcity",
            adventure_type="Beach and ocean",
            climate="Tropical",
            flight="Quick"
        )
        self.destination.save()

        self.destination2 = Destination.objects.create(
            user=self.user,
            city="testcity2",
            country="testcountry2",
            slug="testcity2",
            adventure_type="Beach and ocean",
            climate="Tropical",
            flight="Quick"
        )
        self.destination2.save()

        self.destination_visited = Destination.objects.create(
            user=self.user,
            city="testcityvisited",
            country="testcountryvisited",
            slug="testcityvisited",
            adventure_type="City attractions",
            climate="Subtropical",
            flight="Short",
            has_user_visited=True
        )
        self.destination_visited.save()

        user = User.objects.get(id=1)
        self.blog1 = Blog.objects.create(
            title="4 Resorts Bora Bora",
            slug="4-resorts-bora-bora",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog1.favorite.add(user)
        self.blog1.save()

        self.blog2 = Blog.objects.create(
            title="Top Places to See in Rome",
            slug="top-places-to-see-in-rome",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog2.favorite.add(user)
        self.blog2.save()

        self.blog3 = Blog.objects.create(
            title="5 Reasons to Visit Yellowstone",
            slug="5-reasons-to-visit-yellowstone",
            author=user,
            content="this is test content",
            status=1,
            featured=False,
            blog_img="test.jpg"
        )
        self.blog3.favorite.add(user)
        self.blog3.save()
    
    def test_destination_creation(self):
        """
        Test that destination.has_user_visited is set to False
        when user does not change status to 'visited'.
        """
        destination = Destination.objects.get(pk=1)
        self.assertTrue(Destination.objects.get(pk=1))
        self.assertEqual(destination.has_user_visited, False)
        self.assertEqual(destination.slug, destination.city)

    def test_workspace_home(self):
        """
        Test workspace_home() view function returns
        render.
        """
        self.client.force_login(self.user)
        request = self.factory.get('workspace/')
        request.user = self.user
        response = workspace_home(request)
        self.assertEqual(response.status_code, 200)

    def test_api_home(self):
        """
        Test api_home() view function.
        """
        response = self.client.get(reverse('workspace:api_home'))
        self.assertEqual(response.status_code, 200)

    def test_filter_next_adventure_GET(self):
        """
        Test filter_next_adventure() view function returns form.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_next_adventure'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/filter-next-adventure.html')
        self.assertTrue(response.context['form'])

    def test_filter_next_adventure_POST_with_matching_data(self):
        """
        Test filter_next_adventure() view function returns destinations
        that match form data.
        """
        self.client.force_login(self.user)
        form_data = {
            'adventure': "Beach and ocean",
            'climate': "Tropical",
            'flight': "Quick"
        }
        request = self.factory.post(reverse('workspace:filter_next_adventure'), data=form_data)
        request.user = self.user 
        response = filter_next_adventure(request)
        self.assertEqual(response.status_code, 200)

    def test_filter_next_adventure_POST_without_matching_data(self):
        """
        Test filter_next_adventure() view function redirects when
        form data does not match a Destination object.
        """
        self.client.force_login(self.user)
        form_data = {
            'adventure': "Sport event",
            'climate': "Subtropical",
            'flight': "Short"
        }
        request = self.factory.post(reverse('workspace:filter_next_adventure'), data=form_data)
        request.user = self.user 
        response = filter_next_adventure(request)
        self.assertEqual(response.status_code, 302)
        
    def test_create_destination_GET(self):
        """
        Test create_destination() view function returns form.
        """
        self.client.force_login(self.user)       
        response = self.client.get(reverse('workspace:create_destination'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])

    def test_create_destination_POST(self):
        """
        Test create_destination() view function creates new
        Destination object.
        """
        self.client.force_login(self.user)
        form_data = {
            'user': self.user,
            'city': "testcity2",
            'country': "testcountry2",
            'adventure_type': "Beach and ocean",
            'climate': "Tropical",
            'flight': "Quick"
        }
        request = self.factory.post(reverse('workspace:create_destination'), data=form_data)
        request.user = self.user 
        response = create_destination(request)
        destination = Destination.destination_objects.get(city="testcity2")
        self.assertTrue(destination)

    def test_create_POST_destination_already_exists(self):
        """
        Test create_destination() view function does not 
        create a city that already exists.
        """
        self.client.force_login(self.user)
        form_data = {
            'user': self.user,
            'city': "testcity",
            'country': "testcountry",
            'adventure_type': "Beach and ocean",
            'climate': "Tropical",
            'flight': "Quick"
        }
        request = self.factory.post(reverse('workspace:create_destination'), data=form_data)
        request.user = self.user 
        response = create_destination(request)
        destination = Destination.destination_objects.filter(city="testcity").count()
        self.assertEqual(destination, 1)

    def test_list_destinations(self):
        """
        Test list_destinations() view function returns list of 
        destinations.
        """
        self.client.force_login(self.user)       
        response = self.client.get(reverse('workspace:list_destinations'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['destinations'])

    def test_destination_detail_view_GET(self):
        """
        Test destination_detail() view function returns details of
        selected destination.
        """
        self.client.force_login(self.user)
        request = self.factory.get('details/<str:slug>/', slug=self.destination.slug)
        request.user = self.user 
        response = destination_detail_view(request, slug=self.destination.slug)
        self.assertEqual(response.status_code, 200)

    def test_update_destination_GET(self):
        """
        Test update_destination() view function returns form.
        """
        self.client.force_login(self.user)
        request = self.factory.get('update/<int:pk>/', pk=1)
        request.user = self.user 
        response = update_destination(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_update_destination_GET(self):
        """
        Test update_destination() view function returns form and 
        selected destination to be updated.
        """
        self.client.force_login(self.user)
        destination = self.destination
        request = self.factory.get('update/<int:pk>/', pk=1, instance=destination)
        request.user = self.user 
        response = update_destination(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_delete_destination(self):
        """
        Test delete_destination() view function deletes
        requested destination.
        """
        self.client.force_login(self.user)
        request = self.factory.get('delete/<int:pk>/', pk=1)
        request.user = self.user 
        response = delete_destination(request, pk=1)
        deleted_destination = Destination.objects.get(pk=1)
        self.assertFalse(deleted_destination)
        self.assertRedirects(response, '/workspace/list-destinations/')

    def test_list_visited_destinations(self):
        """
        Test list_visited_destinations() view returns visited 
        destinations.
        """
        self.client.force_login(self.user)       
        response = self.client.get(reverse('workspace:list_visited_destinations'))
        self.assertEqual(response.status_code, 200)

    def test_filter_destiantions_adventure_type(self):
        """
        Test filter_destiantions() view returns destinations with 
        matching adventure type.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_destinations', kwargs={'filter': "Beach-and-ocean"}))
        destination = Destination.destination_objects.filter(adventure_type="Beach and ocean")
        self.assertTrue(destination)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['destinations'])

    def test_filter_destiantions_climate(self):
        """
        Test filter_destiantions() view returns destinations with 
        matching climate.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_destinations', kwargs={'filter': "Tropical"}))
        destination = Destination.destination_objects.filter(climate="Tropical")
        self.assertTrue(destination)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['destinations'])

    def test_filter_destiantions_flight(self):
        """
        Test filter_destiantions() view returns destinations with 
        matching flight.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_destinations', kwargs={'filter': "Quick"}))
        destination = Destination.destination_objects.filter(flight="Quick")
        self.assertTrue(destination)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['destinations'])

    def test_filter_destinations_invalid(self):
        """
        Test filter_destinations() view returns message if destination
        does not match filter.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_destinations', kwargs={'filter': "test"}))
        self.assertEqual(response.status_code, 200)

    def test_filter_visited_destinations_adventure_type(self):
        """
        Test filter_visited_destinations() view returns visited destinations 
        with matching adventure type.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_visited_destinations', kwargs={'filter': "City-attractions"}))
        destination = Destination.visited_destination_objects.filter(adventure_type="City attractions")
        self.assertTrue(destination)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['destinations'])

    def test_filter_visited_destinations_climate(self):
        """
        Test filter_visited_destinations() view returns visited destinations 
        with matching climate.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_visited_destinations', kwargs={'filter': "Subtropical"}))
        destination = Destination.visited_destination_objects.filter(climate="Subtropical")
        self.assertTrue(destination)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['destinations'])

    def test_filter_visited_destinations_flight(self):
        """
        Test filter_visited_destinations() view returns visited destinations 
        with matching flight.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_visited_destinations', kwargs={'filter': "Short"}))
        destination = Destination.visited_destination_objects.filter(flight="Short")
        self.assertTrue(destination)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['destinations'])

    def test_filter_visited_destinations_invalid(self):
        """
        Test filter_visited_destinations() view returns message if destination
        does not match filter.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:filter_visited_destinations', kwargs={'filter': "test"}))
        self.assertEqual(response.status_code, 200)
        
    def test_sort_destinations_ascending(self):
        """
        Test sort_destinations() view returns destinations in
        ascending order by city.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:sort_destinations', kwargs={'sort': "ascending"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/list-destinations.html')
        self.assertTrue(response.context['destinations'])

    def test_sort_destinations_descending(self):
        """
        Test sort_destinations() view returns destinations in
        descending order by city.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:sort_destinations', kwargs={'sort': "descending"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/list-destinations.html')
        self.assertTrue(response.context['destinations'])

    def test_sort_destinations_country_ascending(self):
        """
        Test sort_destinations() view returns destinations in
        ascending order by country.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:sort_destinations', kwargs={'sort': "country-a"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/list-destinations.html')
        self.assertTrue(response.context['destinations'])
    
    def test_sort_destinations_country_descending(self):
        """
        Test sort_destinations() view returns destinations in
        descending order by country.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:sort_destinations', kwargs={'sort': "country-d"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/list-destinations.html')
        self.assertTrue(response.context['destinations'])
        
    def test_sort_visited_destinations_ascending(self):
        """
        Test sort_visited_destinations() view returns visited destinations in
        ascending order by city.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:sort_visited_destinations', kwargs={'sort': "ascending"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/list-visited-destinations.html')
        self.assertTrue(response.context['destinations'])

    def test_sort_visited_destinations_descending(self):
        """
        Test sort_visited_destinations() view returns visited destinations in
        descending order by city.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:sort_visited_destinations', kwargs={'sort': "country-d"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/list-visited-destinations.html')
        self.assertTrue(response.context['destinations'])

    def test_sort_visited_destinations_country_ascending(self):
        """
        Test sort_visited_destinations() view returns visited destinations in
        ascending order by country.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:sort_visited_destinations', kwargs={'sort': "country-a"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/list-visited-destinations.html')
        self.assertTrue(response.context['destinations'])

    def test_sort_visited_destinations_country_descending(self):
        """
        Test sort_visited_destinations() view returns visited destinations in
        descending order by country.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('workspace:sort_visited_destinations', kwargs={'sort': "descending"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/list-visited-destinations.html')
        self.assertTrue(response.context['destinations'])
