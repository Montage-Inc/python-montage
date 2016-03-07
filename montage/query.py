import copy
import datetime

__all__ = ('Query',)


class Field(object):
    modifiers = ('date', 'time', 'year', 'month', 'day', 'hours', 'minutes',
        'seconds', 'day_of_month', 'day_of_year', 'timezone')
    operators = ('eq', 'ne', 'lt', 'le', 'gt', 'ge', 'ieq', 'in', 'contains',
        'regex', 'starts', 'istarts', 'ends', 'iends', 'intersects', 'includes')

    def __init__(self, field):
        self.field = field

    def __eq__(self, other):
        return self.eq(other)

    def __ne__(self, other):
        return self.ne(other)

    def __lt__(self, other):
        return self.lt(other)

    def __le__(self, other):
        return self.le(other)

    def __gt__(self, other):
        return self.gt(other)

    def __ge__(self, other):
        return self.ge(other)

    def in_(self, value):
        return getattr(self, 'in')(value)

    def __getattr__(self, attr):
        if attr in self.operators:
            return self._operator(attr)
        if attr in self.modifiers:
            return self._modifier(attr)
        raise AttributeError("'row' object has no attribute '{0}'".format(attr))

    def _modifier(self, modifier):
        def inner():
            return Field('{0}.${1}'.format(self.field, modifier))
        return inner

    def _operator(self, operator):
        def inner(value):
            return [self.field, ['${0}'.format(operator), self._coerce(value)]]
        return inner

    def _coerce(self, value):
        if isinstance(value, datetime.datetime):
            return ['$datetime', str(value)]
        if isinstance(value, datetime.date):
            return ['$date', str(value)]
        if isinstance(value, datetime.time):
            return ['$time', str(value)]
        return value


class Query(object):
    def __init__(self, schema):
        self.schema = schema
        self.terms = []

    @classmethod
    def AND(cls, *args):
        return ['$and', args]

    @classmethod
    def OR(cls, *args):
        return ['$or', args]

    @classmethod
    def NOT(cls, *args):
        return ['$or', args]

    def _clone(self):
        query = type(self)(self.schema)
        query.terms.extend(copy.deepcopy(self.terms))
        return query

    def as_dict(self):
        return {
            '$schema': self.schema,
            '$query': copy.deepcopy(self.terms)
        }

    def get(self, id):
        self.terms.append(['$get', id])
        return self._clone()

    def get_all(self, *ids, **kwargs):
        index = kwargs.pop('index', 'id')
        self.terms.append(['$get_all', [index, ids]])
        return self._clone()

    def filter(self, *filters):
        self.terms.append(['$filter', filters])
        return self._clone()

    def has_fields(self, *fields):
        self.terms.append(['$has_fields', fields])
        return self._clone()

    def with_fields(self, *fields):
        self.terms.append(['$with_fields', fields])
        return self._clone()

    def order_by(self, field, ordering=None):
        ordering = ordering or 'asc'
        if ordering not in ('asc', 'desc'):
            raise ValueError('.order_by ordering must be desc or asc')
        self.terms.append(['$order_by', field, ordering])
        return self._clone()

    def skip(self, num):
        self.terms.append(['$skip', num])
        return self._clone()

    def limit(self, num):
        self.terms.append(['$limit', num])
        return self._clone()

    def slice(self, start, end):
        self.terms.append(['$slice', [start, end]])
        return self._clone()

    def nth(self, num):
        self.terms.append(['$nth', num])
        return self._clone()

    def sample(self, num):
        self.terms.append(['$sample', num])
        return self._clone()

    def pluck(self, *fields):
        self.terms.append(['$pluck', fields])
        return self._clone()

    def without(self, *fields):
        self.terms.append(['$without', fields])
        return self._clone()

    def count(self, value=None):
        if value:
            self.terms.append(['$count', value])
        else:
            self.terms.append(['$count'])
        return self._clone()

    def sum(self, field):
        self.terms.append(['$sum', field])
        return self._clone()

    def avg(self, field):
        self.terms.append(['$avg', field])
        return self._clone()

    def min(self, field):
        self.terms.append(['$min', field])
        return self._clone()

    def max(self, field):
        self.terms.append(['$max', field])
        return self._clone()

    def between(self, start, end, index=None):
        value = [start, end] if index is None else [start, end, index]
        self.terms.append(['$between', value])
        return self._clone()
