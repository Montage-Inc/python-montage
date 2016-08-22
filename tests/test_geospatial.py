from decimal import Decimal

import pytest

import montage

from .utils import MontageTests


class GeospatialTests(MontageTests):
    def test_validate_geometry_error(self):
        geometry = {
            'type': 'Point',
            'coordinates': 'bad data'
        }
        with pytest.raises(montage.ValidationError):
            montage.geospatial.validate_geojson(geometry)

    def test_validate_geometry(self):
        geometry = {
            'type': 'Point',
            'coordinates': [-119.772591, 36.746841]
        }
        montage.geospatial.validate_geojson(geometry)


    def test_validate_geometry_decimal(self):
        geometry = {
            'type': 'Point',
            'coordinates': [Decimal('-119.772591'), Decimal('36.746841')]
        }
        montage.geospatial.validate_geojson(geometry)

    def test_convert_polygon(self):
        geometry = {
            'type': 'Polygon',
            'coordinates': [
                [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]
            ]
        }

        polygon_list = montage.geospatial.convert_polygon(geometry)
        assert polygon_list == [geometry]

    def test_convert_multipolygon(self):
        geometry =  {
            'type': 'MultiPolygon',
            'coordinates': [
                [
                    [[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]
                ],
                [
                    [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                    [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]
                ]
            ]
        }

        polygon_list = montage.geospatial.convert_polygon(geometry)
        expected_list = [
            {'type': 'Polygon', 'coordinates': geometry['coordinates'][0]},
            {'type': 'Polygon', 'coordinates': geometry['coordinates'][1]},
        ]
        assert polygon_list == expected_list
