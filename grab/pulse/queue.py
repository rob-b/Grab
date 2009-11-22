import beanstalkc


class SocketError(beanstalkc.SocketError):
    pass

def add(name):
    try:
        beanstalk = beanstalkc.Connection()
    except beanstalkc.SocketError, e:
        raise SocketError(e.args)
    else:
        beanstalk.put(str(name))


