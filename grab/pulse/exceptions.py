from django.utils.translation import ugettext as _


class PulseError(Exception):
    pass


class SocketError(PulseError):

    def __init__(self, *args, **kwargs):
        super(SocketError, self).__init__(*args, **kwargs)
        if self.args[0] == 111:
            self.args = (111, _('Connection refused. Are you sure that'
                                ' beanstalkd is running?'))

