import json
import unittest

import montage

__all__ = ('MontageTests', 'make_response', 'USER', 'SCHEMAS', 'FILES')


def make_response(data):
    return json.dumps({'data': data})


USER = {
    'id': 1,
    'full_name': 'Joe McTest',
    'email': 'test@example.com',
    'token': 'f47d2208-1b24-4c65-afb8-4a9ed02b68ac',
}


ROLE = {
    'name': 'TestUsers',
    'users': [1]
}

POLICY = {
    'id': '5f3eab03-1d70-4cf1-a79f-56a68118eb09',
    'description': 'Default policy',
    'policy': {
        'version': 'v1',
        'grant': True,
        'statements': [
            {
                'action': ['*'],
                'resource': '*',
                'principal': ['montage:role:Admins'],
            },
            {
                'action': [
                    'montage:*:list',
                    'montage:*:detail',
                    'montage:documents:read',
                ],
                'resource': '*',
                'principal': ['montage:user:id:*'],
            }
        ]
    }
}

SCHEMAS = [{
    'id': 'c449d88b-7eec-4c23-ba87-45057735f561',
    'name': 'movies',
    'fields': [
        {'name': 'title', 'datatype': 'text', 'indexed': False, 'required': True},
        {'name': 'year', 'datatype': 'numeric', 'indexed': True, 'required': True},
        {'name': 'rank', 'datatype': 'numeric', 'indexed': True, 'required': True},
        {'name': 'rating', 'datatype': 'numeric', 'indexed': True, 'required': True},
        {'name': 'votes', 'datatype': 'numeric', 'indexed': False, 'required': True}
    ],
    'links': {
        'self': 'https://testco.mntge.com/api/v1/schemas/movies/',
        'save': 'https://testco.mntge.com/api/v1/schemas/movies/save/',
    }
}]

DOCUMENTS = [
    {'id': '1ff3f165-1df7-4b7e-8750-8e9a1a5dab2d', 'title': 'The Shawshank Redemption', 'year': 1994, 'rank': 1, 'rating': 9.2, 'votes': 1262930},
    {'id': 'c8c6c982-8106-4819-8a46-a09baeff5ab8', 'title': 'The Godfather', 'year': 1972, 'rank': 2, 'rating': 9.2, 'votes': 872079},
    {'id': 'dd53773a-cc2a-4ce8-b139-a565fec70622', 'title': 'The Godfather: Part II', 'year': 1974, 'rank': 3, 'rating': 9.0, 'votes': 578821},
    {'id': '31cc5aae-1a76-42fb-ad8e-156e5c2d8449', 'title': 'The Dark Knight', 'year': 2008, 'rank': 4, 'rating': 8.9, 'votes': 1224954},
    {'id': 'f2733e17-9775-4bcb-add9-e76ab32f6184', 'title': 'Pulp Fiction', 'year': 1994, 'rank': 5, 'rating': 8.9, 'votes': 968331, },
    {'id': '8cc831f4-647e-450e-87c3-726ef61d0c0a', 'title': 'Il buono, il brutto, il cattivo.', 'year': 1966, 'rank': 6, 'rating': 8.9, 'votes': 378441, },
    {'id': '690fff76-e35a-46da-a755-a90975fc15f7', 'title': "Schindler's List", 'year': 1993, 'rank': 7, 'rating': 8.9, 'votes': 637203, },
    {'id': 'bab5b1a5-03a9-4867-860c-d2bc8e028c5f', 'title': '12 Angry Men', 'year': 1957, 'rank': 8, 'rating': 8.9, 'votes': 316018, },
    {'id': 'abb4b97c-0522-49e8-8528-0a047c13a5f2', 'title': 'The Lord of the Rings: The Return of the King', 'year': 2003, 'rank': 9, 'rating': 8.9, 'votes': 899183, },
    {'id': 'd3b0963a-47d4-464b-a425-59bdd242e086', 'title': 'Fight Club', 'year': 1999, 'rank': 10, 'rating': 8.8, 'votes': 960982, },
]

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


class MontageTests(unittest.TestCase):
    def setUp(self):
        self.client = montage.Client('testco', token=USER['token'])
        self.client.host = 'hexxie.com'
        super(MontageTests, self).setUp()
