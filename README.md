python-montage
==============

Python library for Montage

Usage
-----

```
>>> import montage
>>> client = montage.Client(subdomain[, token])
>>> client.authenticate(email, password)  # sets client.token
>>> client.user()

# Users
>>> client.user.info()

# Schemas
>>> client.schemas.all()
>>> client.schemas.get('schema')

# Data
>>> query = montage.Query('schema')
>>> query = query.filter(**kwargs)
>>> query = query.limit(10)
>>> query = query.skip(10)
>>> query = query.order_by(field[, ordering=asc|desc])

>>> client.data.query(query)
>>> client.data.query(q1=query1, q2=query2)

>>> client.data.save(schema, *documents)
>>> client.data.get(schema, document_id)
>>> client.data.delete(schema, document_id)

# Files
>>> client.files.all()
>>> client.files.save(*files)
>>> client.files.get(file_id)
>>> client.files.delete(file_id)
```
