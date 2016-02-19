import json
import unittest

import montage

__all__ = ('MontageTests', 'make_response', 'SCHEMAS', 'FILES')


class MontageTests(unittest.TestCase):
    def setUp(self):
        self.client = montage.Client('testco', url='hexxie.com')
        super(MontageTests, self).setUp()


def make_response(data):
    return json.dumps({'data': data})


SCHEMAS = [{
    'id': 'c449d88b-7eec-4c23-ba87-45057735f561',
    'name': 'movies',
    'fields': [{
        'name': 'rank',
        'datatype': 'numeric',
        'indexed': True,
        'required': True
    }, {
        'name': 'studio_id',
        'datatype': 'text',
        'indexed': False,
        'required': False
    }, {
        'name': 'rating',
        'datatype': 'numeric',
        'indexed': True,
        'required': True
    }, {
        'name': 'title',
        'datatype': 'text',
        'indexed': False,
        'required': True
    }, {
        'name': 'votes',
        'datatype': 'numeric',
        'indexed': False,
        'required': True
    }, {
        'name': 'year',
        'datatype': 'numeric',
        'indexed': True,
        'required': True
    }],
    'links': {
        'self': 'https://testco.mntge.com/api/v1/schemas/movies/',
        'save': 'https://testco.mntge.com/api/v1/schemas/movies/save/',
    }
}]

FILES = [{
    'id': '3c49f9c8-2ddc-4e96-a732-b1f2d61c04b8',
    'name': 'python-powered_bCiSyDG.png',
    'size': 2725,
    'url': '/storage/da51fc54-92a5-49bc-99c3-441c5fff81b5/2016/07/python-powered_bCiSyDG.png',
    'checksum': '5eebd16367edcbfb098dc63142d1030c894a8de0'
}, {
    'id': '6232019c-4570-4488-9240-92db2adf8a20',
    'name': 'django-project_Gu46E7m.gif',
    'size': 1966,
    'url': '/storage/da51fc54-92a5-49bc-99c3-441c5fff81b5/2016/07/django-project_Gu46E7m.gif',
    'checksum': 'eb1e39196ee01c5c06dfe481922c5bca6b4fe777'
}, {
    'id': '01423e9f-a2ed-40e9-9308-c85777986a33',
    'name': 'hello-world_MxSO6sX.txt',
    'size': 12,
    'url': '/storage/da51fc54-92a5-49bc-99c3-441c5fff81b5/2016/07/django-project_Gu46E7m.gif',
    'checksum': 'b7e23ec29af22b0b4e41da31e868d57226121c84'
}]
