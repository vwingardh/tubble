from .models import Destination


def destinations(request):
    """
    Returns all destination objects.
    """
    return {'destinations_all': Destination.destination_objects.all()}

def visited_destinations(request):
    """
    Returns all visited destination objects.
    """
    return {'visited_destinations_all': Destination.visited_destination_objects.all()}

def adventure_type(request):
    """
    Returns adventure_type choices from the Destination model to be
    used in templates for filter drop down.
    """
    choices = []
    adventure_choices = Destination._meta.get_field('adventure_type').choices
    for a in adventure_choices:
        i = a[1]
        choices.append(i)
    return {'adventure_type': choices }

def climate(request):
    """
    Returns climate choices from the Destination model to be
    used in templates for filter drop down.
    """
    choices = []
    climate_choices = Destination._meta.get_field('climate').choices
    for c in climate_choices:
        i = c[1]
        choices.append(i)
    return {'climate': choices }

def flight(request):
    """
    Returns flight choices from the Destination model to be
    used in templates for filter drop down.
    """
    choices = []
    flight_choices = Destination._meta.get_field('flight').choices
    for f in flight_choices:
        i = f[1]
        choices.append(i)
    return {'flight': choices }
