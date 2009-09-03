from feeds.models import Feed

def feeds(request):
    return {'feeds': Feed.objects.all()}
