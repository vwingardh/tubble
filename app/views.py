from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from workspace.models import Destination
from blog.models import Blog
from django.db.models import Count
from . forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            messages.success(request, 'Your message has been received.')
            return redirect('app:contact')
    else:
        form = ContactForm()
    return render(request, 'app/resources/contact-us.html', {'form': form})


def index(request):
    destinations = Destination.destination_objects.values(
        'city', 
        'country'
    ).annotate(count=Count('city')).order_by('-count')[0:6]
    context = {
        'destinations': destinations
    }
    return render(request, 'app/index.html', context)
    

def features(request):
    return render(request, 'app/resources/features.html')


def pricing(request):
    return render(request, 'app/resources/pricing.html')


def preview(request):
    return render(request, 'app/resources/preview.html')


def about_tubble(request):
    return render(request, 'app/resources/about-us.html')


def careers(request):
    return render(request, 'app/resources/careers.html')


def mobile_app(request):
    return render(request, 'app/resources/mobile-app.html')
