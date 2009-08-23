from django.conf import settings
from django.core.files.storage import FileSystemStorage

class AttachmentStorage(FileSystemStorage):
    """Save user generated content to a directory outside of the normal
    media_root

    Can optionally overwrite attachments on save"""

    def __init__(self,
                 location=settings.ATTACHMENT_ROOT,
                 base_url=settings.ATTACHMENT_URL,
                 overwrite=False):

        self.overwrite = overwrite
        super(AttachmentStorage, self).__init__(location, base_url)

    def save(self, name, content):

        if self.overwrite:
            self.delete(name)
        return super(AttachmentStorage, self).save(name, content)

