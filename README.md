python-montage
==============

Python library for Montage

Usage
-----

```
>>> from montage import MontageAPI
>>> montage = MontageAPI(subdomain[, token])
>>> montage.authenticate(email, password)  # sets self.token

# Schemas
>>> schema = montage.schema('foo')
>>> schema.detail()
>>> schema.alter()  # Someday...

# Documents
>>> query = schema.documents.query()  # Effectively, fetch all
>>> query = query.filter(**kwargs)
>>> query = query.limit(0)
>>> query = query.offset(0)
>>> query = query.order_by(field[, ordering=asc|desc])
>>> for document in query:
...     print document['id']

>>> schema.documents.save(*documents)
>>> schema.documents.detail(document_id)
>>> schema.documents.delete(document_id)

# Files
>>> montage.files.list()
>>> montage.files.upload(*files)
>>> montage.files.detail(file_id)
>>> montage.files.delete(file_id)
```
