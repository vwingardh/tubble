from django_countries import countries

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, UserProfileForm
from .models import User, UserProfile
from workspace.models import Destination


@login_required
def user_view_profile(request, username):
    user = User.objects.get(username=username)
    total_visited_destinations_created = Destination.visited_destination_objects.filter(user=user.id).count()
    total_destinations_created = Destination.destination_objects.filter(user=user.id).count()
    context = {
        'total_visited_destinations_created': total_visited_destinations_created,
        'total_destinations_created': total_destinations_created,
        'user': user
    }
    return render(request, 'account/public-user-profile.html', context)


def user_registration(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.password1 = form.cleaned_data['password1']
            user.password2 = form.cleaned_data['password2']
            same_password = RegisterUserForm.is_password_match(user.password1, user.password2)
            if same_password == True:
                user.set_password(user.password1)
                user.is_active = True
                user.save()
                login(request, user)          
                return redirect('account:user_update_profile')
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_update_profile(request):
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.get_user_profile(user)
    countries_visited = UserProfile.get_country_list(user)
    # POST updated form data
    if request.method == 'POST':
        if user_profile:
            profile = UserProfile.objects.get(user=user.id)
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
        # POST initial form data on first login
        else:
            form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_form = form.save(commit=False)
            profile_form.profile_img = form.cleaned_data['profile_img']
            profile_form.location = form.cleaned_data['location']
            profile_form.gender = form.cleaned_data['gender']
            profile_form.age = form.cleaned_data['age']
            profile_form.countries_visited = form.cleaned_data['countries_visited']
            profile_form.bio = form.cleaned_data['bio']
            profile_form.save()
            UserProfile.set_adventure_level(user)
            return redirect('workspace:workspace_home')
    else:
        form = UserProfileForm()
    context = {
        'user': user, 
        'countries': countries, 
        'form': form, 
        'countries_visited': countries_visited
    }
    return render(request, 'account/update-profile.html', context)
