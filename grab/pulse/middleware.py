from pulse.views import queue_error
from pulse.exceptions import PulseError

class QueueMiddleware(object):

    def process_exception(self, request, exception):
        if isinstance(exception, PulseError):
            return queue_error(request, exception)
        return None
