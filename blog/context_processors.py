from blog.models import Blog


def blog_bora(request):
    """
    Returns 'Bora Bora' blog post, 1 of 3 standard blog posts for template rendering.
    """
    return {'blog_bora': Blog.objects.get(slug='4-resorts-bora-bora')}

def blog_rome(request):
    """
    Returns 'Rome' blog post, 1 of 3 standard blog posts for template rendering.
    """
    return {'blog_rome': Blog.objects.get(slug='top-places-to-see-in-rome')}

def blog_yellowstone(request):
    """
    Returns 'Yellowstone' blog post, 1 of 3 standard blog posts for template rendering.
    """
    return {'blog_yellowstone': Blog.objects.get(slug='5-reasons-to-visit-yellowstone')}
