from django.conf import settings
from django.core.files.storage import Storage

class MyStorage(Storage):
    def open(self, name, mode='rb'):
        pass

    def save(self, name, content, max_length=None):
        pass

    def url(self, name):
        return 'http://192.168.177.133:8888/' + name
