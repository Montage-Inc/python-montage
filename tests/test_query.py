import montage
import pytest

from .utils import MontageTests


class QueryTests(MontageTests):
    def test_get(self):
        query = montage.Query('movies').get('1234')
        assert query.terms == [['$get', {'key': '1234'}]]

    def test_get_all(self):
        query = montage.Query('movies').get_all('1234', 'abcd')
        assert query.terms == [['$get_all', {
            'keys': ('1234', 'abcd')
        }]]

    def test_between(self):
        query = montage.Query('movies').between(0, 10, index='rank')
        assert query.terms == [['$between', {
            'lower_key': 0,
            'upper_key': 10,
            'index': 'rank',
        }]]

    def test_has_fields(self):
        query = montage.Query('movies').has_fields('title', 'rating')
        assert query.terms == [['$has_fields', {
            'fields': ('title', 'rating')
        }]]

    def test_with_fields(self):
        query = montage.Query('movies').with_fields('title', 'rating')
        assert query.terms == [['$with_fields', {
            'fields': ('title', 'rating')
        }]]

    def test_order_by_default(self):
        query = montage.Query('movies').order_by('rating')
        assert query.terms == [['$order_by', {'key': 'rating'}]]

    def test_order_by_index(self):
        query = montage.Query('movies').order_by(index='rating')
        assert query.terms == [['$order_by', {'index': 'rating'}]]

    def test_order_by_asc(self):
        query = montage.Query('movies').order_by('rating', ordering='asc')
        assert query.terms == [['$order_by', {
            'key': 'rating',
            'ordering': '$asc'
        }]]

    def test_order_by_desc(self):
        query = montage.Query('movies').order_by('rating', ordering='desc')
        assert query.terms == [['$order_by', {
            'key': 'rating',
            'ordering': '$desc'
        }]]

    def test_skip(self):
        query = montage.Query('movies').skip(10)
        assert query.terms == [['$skip', {'n': 10}]]

    def test_limit(self):
        query = montage.Query('movies').limit(10)
        assert query.terms == [['$limit', {'n': 10}]]

    def test_slice(self):
        query = montage.Query('movies').slice(10, 20)
        assert query.terms == [['$slice', {
            'start_offset': 10,
            'end_offset': 20,
        }]]

    def test_nth(self):
        query = montage.Query('movies').nth(5)
        assert query.terms == [['$nth', {'n': 5}]]

    def test_sample(self):
        query = montage.Query('movies').sample(20)
        assert query.terms == [['$sample', {'n': 20}]]

    def test_pluck(self):
        query = montage.Query('movies').pluck('name', 'rank', 'rating')
        assert query.terms == [['$pluck', {
            'fields': ('name', 'rank', 'rating')
        }]]

    def test_without(self):
        query = montage.Query('movies').without('votes', 'rank')
        assert query.terms == [['$without', {
            'fields': ('votes', 'rank')
        }]]

    def test_count(self):
        query = montage.Query('movies').count()
        assert query.terms == [['$count']]

    def test_sum(self):
        query = montage.Query('movies').sum('rank')
        assert query.terms == [['$sum', {'field': 'rank'}]]

    def test_avg(self):
        query = montage.Query('movies').avg('rank')
        assert query.terms == [['$avg', {'field': 'rank'}]]

    def test_min(self):
        query = montage.Query('movies').min('rating')
        assert query.terms == [['$min', {'field': 'rating'}]]

    def test_max(self):
        query = montage.Query('movies').max('rating')
        assert query.terms == [['$max', {'field': 'rating'}]]

    def test_get_intersecting(self):
        point = {
            'type': 'Point',
            'coordinates': [-120.34589052200315, 36.12704320788633]
        }
        query = montage.Query('places').get_intersecting(point, 'location')
        assert query.terms == [['$get_intersecting', {
            'geometry': point,
            'index': 'location'
        }]]

    def test_get_nearest(self):
        point = {
            'type': 'Point',
            'coordinates': [-120.34589052200315, 36.12704320788633]
        }
        query = montage.Query('places').get_nearest(point, 'location')
        assert query.terms == [['$get_nearest', {
            'geometry': point,
            'index': 'location'
        }]]


class QueryFilterTests(MontageTests):
    def test_ge(self):
        query = montage.Query('movies').filter(
            montage.Field('rank') >= 3
        )

        expected = {
            '$type': 'query',
            '$schema': 'movies',
            '$query': [
                ['$filter', {'predicate': (
                    ['rank', ['$ge', 3]],
                )}]
            ]
        }

        assert query.as_dict() == expected

    def test_multiple(self):
        query = montage.Query('movies').filter(
            montage.Field('year') >= 1990,
            montage.Field('year') < 2000
        )

        expected = {
            '$type': 'query',
            '$schema': 'movies',
            '$query': [
                ['$filter', {'predicate': (
                    ['year', ['$ge', 1990]],
                    ['year', ['$lt', 2000]],
                )}]
            ]
        }

        assert query.as_dict() == expected

    def test_or(self):
        query = montage.Query('movies').filter(
            montage.Query.OR(
                montage.Field('year') < 1990,
                montage.Field('year') >= 2000,
            )
        )

        expected = {
            '$type': 'query',
            '$schema': 'movies',
            '$query': [
                ['$filter', {'predicate': (
                    ['$or', (
                        ['year', ['$lt', 1990]],
                        ['year', ['$ge', 2000]],
                    )],
                )}]
            ]
        }

        assert query.as_dict() == expected

    def test_default(self):
        query = montage.Query('movies').filter(
            montage.Field('year') == 2000,
            default=True
        )

        expected = {
            '$type': 'query',
            '$schema': 'movies',
            '$query': [
                ['$filter', {
                    'predicate': (
                        ['year', ['$eq', 2000]],
                    ),
                    'default': True
                }]
            ]
        }

        assert query.as_dict() == expected
