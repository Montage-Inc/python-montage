import montage
import pytest

from .utils import MontageTests


class QueryTests(MontageTests):
    def test_get(self):
        query = montage.Query('movies').get('1234')
        assert query.terms == [['$get', '1234']]

    def test_get_all(self):
        query = montage.Query('movies').get_all('1234', 'abcd')
        assert query.terms == [['$get_all', ['id', ('1234', 'abcd')]]]

    def test_has_fields(self):
        query = montage.Query('movies').has_fields('title', 'rating')
        assert query.terms == [['$has_fields', ('title', 'rating')]]

    def test_with_fields(self):
        query = montage.Query('movies').with_fields('title', 'rating')
        assert query.terms == [['$with_fields', ('title', 'rating')]]

    def test_order_by_default(self):
        query = montage.Query('movies').order_by('rating')
        assert query.terms == [['$order_by', 'rating', 'asc']]

    def test_order_by_asc(self):
        query = montage.Query('movies').order_by('rating', 'asc')
        assert query.terms == [['$order_by', 'rating', 'asc']]

    def test_order_by_desc(self):
        query = montage.Query('movies').order_by('rating', 'desc')
        assert query.terms == [['$order_by', 'rating', 'desc']]

    def test_order_by_invalid(self):
        with pytest.raises(ValueError):
            query = montage.Query('movies').order_by('rating', ordering=-1)

    def test_skip(self):
        query = montage.Query('movies').skip(10)
        assert query.terms == [['$skip', 10]]

    def test_limit(self):
        query = montage.Query('movies').limit(10)
        assert query.terms == [['$limit', 10]]

    def test_slice(self):
        query = montage.Query('movies').slice(10, 20)
        assert query.terms == [['$slice', [10, 20]]]

    def test_nth(self):
        query = montage.Query('movies').nth(5)
        assert query.terms == [['$nth', 5]]

    def test_sample(self):
        query = montage.Query('movies').sample(20)
        assert query.terms == [['$sample', 20]]

    def test_pluck(self):
        query = montage.Query('movies').pluck('name', 'rank', 'rating')
        assert query.terms == [['$pluck', ('name', 'rank', 'rating')]]

    def test_without(self):
        query = montage.Query('movies').without('votes', 'rank')
        assert query.terms == [['$without', ('votes', 'rank')]]

    def test_count(self):
        query = montage.Query('movies').count()
        assert query.terms == [['$count']]

    def test_sum(self):
        query = montage.Query('movies').sum('rank')
        assert query.terms == [['$sum', 'rank']]

    def test_avg(self):
        query = montage.Query('movies').avg('rank')
        assert query.terms == [['$avg', 'rank']]

    def test_min(self):
        query = montage.Query('movies').min('rating')
        assert query.terms == [['$min', 'rating']]

    def test_max(self):
        query = montage.Query('movies').max('rating')
        assert query.terms == [['$max', 'rating']]

    def test_between(self):
        query = montage.Query('movies').between(0, 10, 'rank')
        assert query.terms == [['$between', [0, 10, 'rank']]]

    def test_get_intersecting(self):
        point = {
            'type': 'Point',
            'coordinates': [-120.34589052200315, 36.12704320788633]
        }
        query = montage.Query('places').get_intersecting(point, index='location')
        assert query.terms == [['$get_intersecting', ['location', point]]]

    def test_get_nearest(self):
        point = {
            'type': 'Point',
            'coordinates': [-120.34589052200315, 36.12704320788633]
        }
        query = montage.Query('places').get_nearest(point, index='location')
        assert query.terms == [['$get_nearest', ['location', point]]]


class QueryFilterTests(MontageTests):
    def test_ge(self):
        query = montage.Query('movies').filter(
            montage.Field('rank') >= 3
        )

        expected = {
            '$schema': 'movies',
            '$query': [
                ['$filter', (
                    ['rank', ['$ge', 3]],
                )]
            ]
        }

        assert query.as_dict() == expected

    def test_multiple(self):
        query = montage.Query('movies').filter(
            montage.Field('year') >= 1990,
            montage.Field('year') < 2000
        )

        expected = {
            '$schema': 'movies',
            '$query': [
                ['$filter', (
                    ['year', ['$ge', 1990]],
                    ['year', ['$lt', 2000]],
                )]
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
            '$schema': 'movies',
            '$query': [
                ['$filter', (
                    ['$or', (
                        ['year', ['$lt', 1990]],
                        ['year', ['$ge', 2000]],
                    )],
                )]
            ]
        }

        assert query.as_dict() == expected
