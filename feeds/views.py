from grab.utils.helpers import rendered

@rendered
def feed_list(request):
    return 'grab/feed_list.html', {}
