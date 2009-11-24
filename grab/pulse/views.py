from hostel.decorators import rendered

@rendered
def queue_error(request, exception, template_name='pulse/queue_error.html'):
    message = exception.args[1]
    return template_name, {'message': message}

