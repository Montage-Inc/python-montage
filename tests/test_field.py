import datetime
import montage

from .utils import MontageTests


class ModifierTests(MontageTests):
    def test_date(self):
        field = montage.Field('birthday').date()
        field.field == 'birthday.$date'
        ts = datetime.date.today()
        expected = ['birthday.$date', ['$eq', ['$date', str(ts)]]]
        assert field.eq(ts) == (field == ts) == expected


class CoersionTests(MontageTests):
    def test_datetime(self):
        ts = datetime.datetime(2008, 7, 1, 12, 42)
        field = montage.Field('timestamp')
        expected = ['timestamp', ['$eq', ['$datetime', '2008-07-01 12:42:00']]]
        assert (field == ts) == expected

    def test_date(self):
        ts = datetime.date(1987, 7, 24)
        field = montage.Field('timestamp')
        expected = ['timestamp', ['$eq', ['$date', '1987-07-24']]]
        assert (field == ts) == expected

    def test_time(self):
        ts = datetime.time(16, 20)
        field = montage.Field('timestamp')
        expected = ['timestamp', ['$eq', ['$time', '16:20:00']]]
        assert (field == ts) == expected


class OperatorTests(MontageTests):
    def test_eq(self):
        field = montage.Field('x')
        expected = ['x', ['$eq', 'y']]
        assert field.eq('y') == (field == 'y') == expected

    def test_ne(self):
        field = montage.Field('x')
        expected = ['x', ['$ne', 'y']]
        assert field.ne('y') == (field != 'y') == expected

    def test_lt(self):
        field = montage.Field('x')
        expected = ['x', ['$lt', 'y']]
        assert field.lt('y') == (field < 'y') == expected

    def test_le(self):
        field = montage.Field('x')
        expected = ['x', ['$le', 'y']]
        assert field.le('y') == (field <= 'y') == expected

    def test_gt(self):
        field = montage.Field('x')
        expected = ['x', ['$gt', 'y']]
        assert field.gt('y') == (field > 'y') == expected

    def test_ge(self):
        field = montage.Field('x')
        expected = ['x', ['$ge', 'y']]
        assert field.ge('y') == (field >= 'y') == expected

    def test_ieq(self):
        field = montage.Field('x')
        expected = ['x', ['$ieq', 'y']]
        assert field.ieq('y') == expected

    def test_in(self):
        field = montage.Field('x')
        expected = ['x', ['$in', 'y']]
        assert field.in_('y') == getattr(field, 'in')('y') == expected

    def test_match(self):
        field = montage.Field('x')
        expected = ['x', ['$match', '^y$']]
        assert field.match('^y$') == expected

    def test_starts(self):
        field = montage.Field('x')
        expected = ['x', ['$starts', 'y']]
        assert field.starts('y') == expected

    def test_istarts(self):
        field = montage.Field('x')
        expected = ['x', ['$istarts', 'y']]
        assert field.istarts('y') == expected

    def test_ends(self):
        field = montage.Field('x')
        expected = ['x', ['$ends', 'y']]
        assert field.ends('y') == expected

    def test_iends(self):
        field = montage.Field('x')
        expected = ['x', ['$iends', 'y']]
        assert field.iends('y') == expected

    def test_intersects(self):
        point = {'type': 'Point', 'coordinates': [36.7477778, -119.7713889]}
        field = montage.Field('x')
        expected = ['x', ['$intersects', point]]
        assert field.intersects(point) == expected

    def test_includes(self):
        point = {'type': 'Point', 'coordinates': [36.7477778, -119.7713889]}
        field = montage.Field('x')
        expected = ['x', ['$includes', point]]
        assert field.includes(point) == expected
