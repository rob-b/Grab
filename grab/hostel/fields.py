from django.db import models
from hostel.widgets import AdminReadOnlyFileWidget

class ReadOnlyFileField(models.FileField):
    """
    Shows readonly file
    """

    __metaclass__ = models.SubfieldBase
    
    def formfield(self, **kwargs):
        defaults = {'widget' : AdminReadOnlyFileWidget}
        defaults.update(kwargs)
        return super(ReadOnlyFileField, self).formfield(**defaults)
