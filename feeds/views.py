from utils.helpers import rendered
from feeds.models import Feed

@rendered
def feed_list(request):

    feeds = Feed.objects.all()
    return 'grab/feed_list.html', {'feeds': feeds}
