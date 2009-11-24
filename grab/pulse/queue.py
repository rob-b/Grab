import beanstalkc
from pulse.exceptions import SocketError

def add(name):
    try:
        beanstalk = beanstalkc.Connection()
    except beanstalkc.SocketError, e:

        # beanstalk exceptions are kind of nested
        raise SocketError(*e.args[0].args)
    else:
        beanstalk.put(str(name))


