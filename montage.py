#!/usr/bin/env python

import collections
import copy
import requests
from cached_property import cached_property

__version__ = '1.0.0'


class MontageAPI(object):
    domain = 'dev.montagehot.club'
    endpoints = {
        'auth': 'auth/',
        'schema-list': 'schemas/',
        'schema-detail': 'schemas/{schema}/',
        'document-query': 'schemas/{schema}/query/',
        'document-save': 'schemas/{schema}/save/',
        'document-detail': 'schemas/{schema}/{document_id}/',
        'file-list': 'files/',
        'file-detail': 'files/{file_id}',
    }

    def __init__(self, subdomain, token=None):
        self.subdomain = subdomain
        self.token = token

    def url(self, name, **kwargs):
        endpoint = self.endpoints[name].format(**kwargs)
        return 'http://{subdomain}.{domain}/api/v1/{endpoint}'.format(
            subdomain=self.subdomain,
            domain=self.domain,
            endpoint=endpoint,
        )

    def get_headers(self):
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Montage Python v{0}'.format(__version__),
        }
        if self.token:
            headers['Authorization'] = 'Token {0}'.format(self.token)
        return headers

    def request(self, url, method=None, **kwargs):
        method = method or 'get'

        headers = self.get_headers()
        headers.update(kwargs.pop('headers', {}))

        response = requests.request(method, url, headers=headers, **kwargs)
        return response.json()

    def authenticate(self, email, password):
        url = self.url('auth')
        response = self.request(url, 'post', data={
            'username': email,
            'password': password
        })
        self.token = response.get('data', {}).get('token')
        if self.token is None:
            return False
        return True

    def schema(self, name):
        return Schema(name, self)


class Schema(object):
    def __init__(self, name, api):
        self.name = name
        self.api = api

    def detail(self):
        url = self.api.url('schema-detail', schema=self.name)
        return self.api.request(url)

    @cached_property
    def documents(self):
        return Documents(self)


class Documents(object):
    def __init__(self, schema):
        self.schema = schema
        self.api = schema.api

    def query(self):
        return Query(self.schema)

    def save(self, *documents):
        data = documents[0] if len(documents) == 1 else documents
        url = self.api.url('document-save', schema=self.schema.name)
        return self.api.request(url, 'post', json=data)

    def get(self, document_id):
        url = self.api.url('document-detail', schema=self.schema.name,
            document_id=document_id)
        return self.api.request(url).get('data')

    def delete(self, document_id):
        url = self.api.url('document-detail', schema=self.schema.name,
            document_id=document_id)
        return self.api.request(url, 'delete')


class Query(object):
    QueryDescriptor = collections.namedtuple('QueryDescriptor', (
        'filter',
        'limit',
        'offset',
        'order_by',
        'ordering',
    ))

    def __init__(self, schema, **kwargs):
        self.schema = schema
        self.api = schema.api
        self.descriptor = self.get_descriptor(**kwargs)

    def __iter__(self):
        # Use a session to keep the connection open
        session = requests.Session()
        session.headers.update(self.api.get_headers())

        url = self.api.url('document-query', schema=self.schema.name)
        response = session.post(url, json=self.descriptor._asdict()).json()

        # Yield the initial result set
        for document in response['data']:
            yield document

        # Keep fetching results until we hit the end of the cursor
        while response['cursors']['next']:
            url = self.api.url('document-query', schema=self.schema.name)
            response = session.get(url, params={
                'cursor': response['cursors']['next']
            }).json()

            for document in response['data']:
                yield document

        session.close()

    def get_descriptor(self, **kwargs):
        defaults = {
            'filter': {},
            'limit': None,
            'offset': None,
            'order_by': None,
            'ordering': 'asc',
        }
        defaults.update(**kwargs)
        return self.QueryDescriptor(**defaults)

    def clone(self, **kwargs):
        descriptor = copy.deepcopy(self.descriptor._asdict())
        descriptor.update(**kwargs)
        query = type(self)(self.schema, **descriptor)
        return query

    def filter(self, **kwargs):
        filter = self.descriptor.filter
        filter.update(**kwargs)
        return self.clone(filter=filter)

    def limit(self, limit):
        return self.clone(limit=limit)

    def offset(self, offset):
        return self.clone(offset=offset)

    def order_by(self, order_by, ordering=None):
        ordering = ordering or 'asc'
        if ordering not in ('asc', 'desc'):
            raise ValueError('ordering must be "asc" or "desc"')
        return self.clone(order_by=order_by, ordering=ordering)
