from hostel.decorators import rendered

@rendered
def queue_error(request, exception):
    assert False, exception.args

