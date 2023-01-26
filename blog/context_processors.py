from blog.models import Blog


def blog_bora(request):
    """
    Returns 'Bora Bora' blog post, 1 of 3 standard blog posts for template rendering.
    """
    try:
        blog_bora = Blog.objects.get(slug='4-resorts-bora-bora')
        return {'blog_bora': blog_bora}
    except:
        return {'blog_bora': None}
    

def blog_rome(request):
    """
    Returns 'Rome' blog post, 1 of 3 standard blog posts for template rendering.
    """
    try:
        blog_rome = Blog.objects.get(slug='top-places-to-see-in-rome')
        return {'blog_rome': blog_rome}
    except:
        return {'blog_rome': None}
    

def blog_yellowstone(request):
    """
    Returns 'Yellowstone' blog post, 1 of 3 standard blog posts for template rendering.
    """
    try: 
        blog_yellowstone = Blog.objects.get(slug='5-reasons-to-visit-yellowstone')
        return {'blog_yellowstone': blog_yellowstone}
    except:
        return {'blog_yellowstone': None}
    