from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.text import slugify
from django.db.models import Q
from django.contrib import messages
from .forms import DestinationCreateForm, NextAdventureFilterForm
from .models import Destination


@login_required
def workspace_home(request):
    total_bucket = Destination.destination_objects.filter(
        user=request.user.id
        ).count()
    total_visited = Destination.visited_destination_objects.filter(
        user=request.user.id
        ).count()
    context = {
        'total_bucket': total_bucket,
        'total_visited': total_visited
    }
    return render(request, 'workspace/workspace-home.html', context)

def api_home(request):
    return render(request, 'workspace/api-home.html')

@login_required
def filter_next_adventure(request):
    adventure = Destination.get_choices_list(choice_field='adventure_type')
    climate = Destination.get_choices_list(choice_field='climate')
    flight = Destination.get_choices_list(choice_field='flight') 
    if request.method == "POST":
        form = NextAdventureFilterForm(request.POST)
        if form.is_valid():
            adventure = form['adventure'].value()
            climate = form['climate'].value()
            flight = form['flight'].value()
    
            next_destinations = Destination.destination_objects.filter(
                user=request.user.id, 
                adventure_type=adventure, 
                climate=climate, 
                flight=flight
            ).order_by('city')
            if next_destinations:
                return render(
                    request, 
                    'workspace/filter-next-results.html', 
                    {'destinations': next_destinations}
                )
            else:
                messages.error(request, "You have not created a destination meeting this criteria, please try again.")
                return redirect('workspace:filter_next_adventure')
    else:
        form = NextAdventureFilterForm()
    context = {
        'adventure': adventure,
        'flight': flight,
        'climate': climate,
        'form': form
    }
    return render(request, 'workspace/filter-next-adventure.html', context)
    
@login_required
def create_destination(request):
    if request.method == 'POST':
        form = DestinationCreateForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.user = request.user
            destination.slug = slugify(form.cleaned_data['city'])
            destination_has_user_visited = request.POST.get('has_user_visited')
            if destination_has_user_visited == None:
                destination.has_user_visited = False
            else:
                destination.has_user_visited = True
            destination_already_exists = Destination.get_destination_exists(
                city=destination.city.lower(), 
                country=destination.country.lower(),
                user_id=request.user.id
            )
            visited_destination_already_exists = Destination.get_visited_destination_exists(
                city=destination.city.lower(), 
                country=destination.country.lower(),
                user_id=request.user.id
            )
            if destination_already_exists:
                city = destination.city.title()
                country = destination.country.title()
                messages.error(request, f"{city}, {country} has already been created. \nTo move this destination to Visited, please edit the original card.")
                return redirect('workspace:create_destination')
            if visited_destination_already_exists:
                city = destination.city.title()
                country = destination.country.title()
                messages.error(request, f"{city}, {country} has already been created as a visited destination.")
                return redirect('workspace:create_destination')
            destination.save()
            messages.success(request, "Your destination has been saved!")
            return redirect('workspace:create_destination')     
    else:
        form = DestinationCreateForm()
    return render(request, 'workspace/create-destination.html', {'form': form})

@login_required
def list_destinations(request):
    destinations = Destination.destination_objects.filter(
        user=request.user.id
        ).order_by('city')
    return render(
        request, 
        'workspace/list-destinations.html', 
        {'destinations': destinations}
    )

@login_required
def destination_detail_view(request, slug):
    destination = Destination.objects.get(
        Q(user=request.user.id) & Q(slug=slug)
    )
    return render(request, 'workspace/destination-detail-view.html', {'destination': destination})

@login_required
def update_destination(request, pk):
    destination = Destination.objects.get(id=pk)
    if request.method == 'POST':
        form = DestinationCreateForm(
            request.POST, 
            request.FILES, 
            instance=destination
        )
        if form.is_valid():
            destination_form = form.save(commit=False)
            destination_form.slug = slugify(form.cleaned_data['city'].lower())
            current_status = destination.has_user_visited
            destination_has_user_visited = request.POST.get('has_user_visited')           
            if destination_has_user_visited == None:
                destination.has_user_visited = current_status
            form.save()
            messages.success(request, "Destination has been updated!")
            return redirect('workspace:list_destinations')
    else:
        form = DestinationCreateForm()         
    return render(
        request, 
        'workspace/update-destination.html', 
        {'form': form, 'destination': destination}
    )

@login_required
def delete_destination(request, pk):
    destination = Destination.objects.get(id=pk)
    destination.delete()
    messages.success(request, "Destination has been removed.")
    return redirect('workspace:list_destinations')

@login_required
def list_visited_destinations(request):
    destinations = Destination.visited_destination_objects.filter(
        user=request.user.id
        ).order_by('city')
    return render(
        request, 
        'workspace/list-visited-destinations.html', 
        {'destinations': destinations}
    )

@login_required 
def filter_destinations(request, filter):
    filter = filter.replace('-', ' ').capitalize()
    adventure_list = Destination.get_choices_list(choice_field='adventure_type')
    climate_list = Destination.get_choices_list(choice_field='climate')
    flight_list = Destination.get_choices_list(choice_field='flight')
    if filter in adventure_list:
        destinations = Destination.destination_objects.filter(user=request.user.id)
        adventure_destinations = destinations.filter(
            adventure_type=filter
            ).order_by('city')
        if adventure_destinations:
            return render(
                request, 
                'workspace/list-destinations.html', 
                {'destinations': adventure_destinations}
            )
        else:
            messages.error(request, 'No destinations meet this criteria.')
            return render(request, 'workspace/list-destinations.html')
    elif filter in climate_list:
        destinations = Destination.destination_objects.filter(user=request.user.id)
        climate_destinations = destinations.filter(climate=filter).order_by('city')
        if climate_destinations:
            return render(
                request, 
                'workspace/list-destinations.html', 
                {'destinations': climate_destinations}
            )
        else:
            messages.error(request, 'No destinations meet this criteria.')
            return render(request, 'workspace/list-destinations.html')
    elif filter in flight_list:
        destinations = Destination.destination_objects.filter(user=request.user.id)
        flight_destinations = destinations.filter(flight=filter).order_by('city')
        if flight_destinations:
            return render(
                request, 
                'workspace/list-destinations.html', 
                {'destinations': flight_destinations}
            )
        else:
            messages.error(request, 'No destinations meet this criteria.')
            return render(request, 'workspace/list-destinations.html')
    else:
        messages.error(request, 'An error occurred, please try again.')
        return render(request, 'workspace/list-destinations.html')

@login_required
def filter_visited_destinations(request, filter):
    filter = filter.replace('-', ' ').capitalize()
    adventure_list = Destination.get_choices_list(choice_field='adventure_type')
    climate_list = Destination.get_choices_list(choice_field='climate')
    flight_list = Destination.get_choices_list(choice_field='flight')
    if filter in adventure_list:
        destinations = Destination.visited_destination_objects.filter(user=request.user.id)
        adventure_destinations = destinations.filter(
            adventure_type=filter
            ).order_by('city')
        if adventure_destinations:
            return render(
                request, 
                'workspace/list-visited-destinations.html', 
                {'destinations': adventure_destinations}
            )
        else:
            messages.error(request, 'No destinations meet this criteria.')
            return render(request, 'workspace/list-visited-destinations.html')
    elif filter in climate_list:
        destinations = Destination.visited_destination_objects.filter(user=request.user.id)
        climate_destinations = destinations.filter(climate=filter).order_by('city')
        if climate_destinations:
            return render(
                request, 
                'workspace/list-visited-destinations.html', 
                {'destinations': climate_destinations}
            )
        else:
            messages.error(request, 'No destinations meet this criteria.')
            return render(request, 'workspace/list-visited-destinations.html')
    elif filter in flight_list:
        destinations = Destination.visited_destination_objects.filter(user=request.user.id)
        flight_destinations = destinations.filter(
            flight=filter
            ).order_by('city')
        if flight_destinations:
            return render(
                request, 
                'workspace/list-visited-destinations.html', 
                {'destinations': flight_destinations}
            )
        else:
            messages.error(request, 'No destinations meet this criteria.')
            return render(request, 'workspace/list-visited-destinations.html')
    else:
        messages.error(request, 'An error occurred, please try again.')
        return render(request, 'workspace/list-visited-destinations.html')

@login_required
def sort_destinations(request, sort):
    if sort == 'ascending':
        destinations = Destination.destination_objects.filter(
            user=request.user.id
            ).order_by('city')
    elif sort == 'descending':
        destinations = Destination.destination_objects.filter(
            user=request.user.id
            ).order_by('-city')
    elif sort == 'country-a':
        destinations = Destination.destination_objects.filter(
            user=request.user.id
            ).order_by('country')
    elif sort == 'country-d':
        destinations = Destination.destination_objects.filter(
            user=request.user.id
            ).order_by('-country')
    return render(
        request, 
        'workspace/list-destinations.html', 
        {'destinations': destinations}
    )

@login_required
def sort_visited_destinations(request, sort):
    if sort == 'ascending':
        destinations = Destination.visited_destination_objects.filter(
            user=request.user.id
            ).order_by('city')
    elif sort == 'descending':
        destinations = Destination.visited_destination_objects.filter(
            user=request.user.id
            ).order_by('-city')
    elif sort == 'country-a':
        destinations = Destination.visited_destination_objects.filter(
            user=request.user.id
            ).order_by('country')
    elif sort == 'country-d':
        destinations = Destination.visited_destination_objects.filter(
            user=request.user.id
            ).order_by('-country')
    return render(
        request, 
        'workspace/list-visited-destinations.html', 
        {'destinations': destinations}
    )
