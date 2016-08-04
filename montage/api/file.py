import mimetypes
import warnings


class FileAPI(object):
    def __init__(self, client):
        self.client = client

    def list(self, **kwargs):
        return self.client.request('files', params=kwargs)

    def get(self, file_id):
        endpoint = 'files/{0}'.format(file_id)
        return self.client.request(endpoint)

    def delete(self, file_id):
        endpoint = 'files/{0}'.format(file_id)
        return self.client.request(endpoint, method='delete')

    def remove(self, file_id):
        warnings.warn('The function remove() is deprecated, use delete().',
        DeprecationWarning, stacklevel=2)
        return self.delete(file_id)

    def save(self, *files):
        '''
            Each file is extected to be a tuple of (name, content), where
            content is a file-like object or the contents as a string.

            client.files.save(('foo.txt', open('/path/to/foo.txt')))
            client.files.save(('foo.txt', StringIO('This is foo.txt')))
            client.files.save(('foo.txt', 'This is foo.txt'))
        '''
        file_list = []
        for name, contents in files:
            content_type = mimetypes.guess_type(name)[0]
            file_list.append(('file', (name, contents, content_type)))
        return self.client.request('files', 'post', files=file_list)
