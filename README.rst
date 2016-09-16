==============
python-montage
==============

.. image:: https://circleci.com/gh/Montage-Inc/python-montage/tree/develop.svg?style=shield
   :target: https://circleci.com/gh/Montage-Inc/python-montage/tree/develop
   :alt: CircleCI

.. image:: https://codecov.io/github/Montage-Inc/python-montage/coverage.svg?branch=develop
   :target: https://codecov.io/github/Montage-Inc/python-montage?branch=develop
   :alt: Coverage

Python library for Montage

Usage
=====

::

    >>> import montage
    >>> client = montage.Client(subdomain[, token])
    >>> client.authenticate(email, password)  # sets client.token

    # Current user
    >>> client.user()

    # Querying and scripting
    >>> query = (montage.Query('movies')
            .order_by(index='year')
            .filter(
                montage.Field('year') >= 1990
                montage.Field('year') < 2000
            )
        )
    >>> script = montage.Script('imdb/fetch-reviews.py', environ={
            'IMDB_MIN_SCORE': 8
        })
    >>> client.run(nineties_movies=query, reviews=script)
    {
        "data": {
            "nineties_movies": [ ... ],
            "reviews": " ... ",
        }
    }

    # Schemas
    >>> client.schemas.list()
    >>> client.schemas.get('schema')

    # Data
    >>> client.documents.save(schema, *documents)
    >>> client.documents.get(schema, document_id)
    >>> client.documents.replace(schema, document)
    >>> client.documents.update(schema, document)
    >>> client.documents.delete(schema, document_id)

    # Files
    >>> client.files.list()
    >>> client.files.save(*files)
    >>> client.files.get(file_id)
    >>> client.files.delete(file_id)

    # Users
    >>> client.users.list()
    >>> client.users.list(email__endswith='gmail.com')
    >>> client.users.create(
    ...     full_name='Test User',
    ...     email='test@example.com',
    ...     password='letmein'
    ... )
    >>> client.users.get(user_id)
    >>> client.users.update(user_id, password='changeme')
    >>> client.users.delete(user_id)

    # Roles
    >>> client.roles.list()
    >>> client.roles.create(name='admins', add_users=['<user_id>'])
    >>> client.roles.get('admins')
    >>> client.roles.update('admins',
            add_users=['<user_id>'],
            remove_users=['<user_id>']
        )
    >>> client.roles.delete('admins')
