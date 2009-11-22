class QueueMiddleware(object):

    def process_exception(self, request, exception):
        assert False, exception.args
