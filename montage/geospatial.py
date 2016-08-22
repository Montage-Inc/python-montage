import jsonschema

from .errors import ValidationError

# JSON-Schema definition for the GeoJSON types supported by Montage
# https://github.com/fge/sample-json-schemas/blob/master/geojson/geometry.json
geojson_schema = jsonschema.Draft4Validator({
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'title': 'Geometry',
    'description': 'One geometry as defined by GeoJSON',
    'type': 'object',
    'required': ['type', 'coordinates'],
    'oneOf': [
        {
            'title': 'Point',
            'properties': {
                'type': {'enum': ['Point']},
                'coordinates': {'$ref': '#/definitions/position'}
            }
        },
        { # Not (yet) supported by Montage
            'title': 'MultiPoint',
            'properties': {
                'type': {'enum': ['MultiPoint']},
                'coordinates': {'$ref': '#/definitions/positionArray'}
            }
        },
        {
            'title': 'LineString',
            'properties': {
                'type': {'enum': ['LineString']},
                'coordinates': {'$ref': '#/definitions/lineString'}
            }
        },
        { # Not (yet) supported by Montage
            'title': 'MultiLineString',
            'properties': {
                'type': {'enum': ['MultiLineString']},
                'coordinates': {
                    'type': 'array',
                    'items': {'$ref': '#/definitions/lineString'}
                }
            }
        },
        {
            'title': 'Polygon',
            'properties': {
                'type': {'enum': ['Polygon']},
                'coordinates': {'$ref': '#/definitions/polygon'}
            }
        },
        { # Not (yet) supported by Montage
            'title': 'MultiPolygon',
            'properties': {
                'type': {'enum': ['MultiPolygon']},
                'coordinates': {
                    'type': 'array',
                    'items': {'$ref': '#/definitions/polygon'}
                }
            }
        },
        { # Custom implementation to convert a GeoJSON-esque data structure into a circle
            'title': 'Circle',
            'properties': {
                'type': {'enum': ['Circle']},
                'coordinates': {'$ref': '#/definitions/position'},
                'radius': {'type': 'number'},
                'num_vertices': {'type': 'number'},
                'geo_system': {'enum': ['WGS84', 'unit_sphere']},
                'unit': {'enum': ['m', 'km', 'mi', 'nm', 'ft']},
                'fill': {'type': 'boolean'},
            },
            'additionalProperties': False,
            'required': ['type', 'coordinates', 'radius'],
        },
    ],
    'definitions': {
        'position': {
            'description': 'A single position',
            'type': 'array',
            'minItems': 2,
            'items': [{'type': 'number'}, {'type': 'number'}],
            'additionalItems': False
        },
        'positionArray': {
            'description': 'An array of positions',
            'type': 'array',
            'items': {'$ref': '#/definitions/position'}
        },
        'lineString': {
            'description': 'An array of two or more positions',
            'allOf': [
                {'$ref': '#/definitions/positionArray'},
                {'minItems': 2}
            ]
        },
        'linearRing': {
            'description': 'An array of four positions where the first equals the last',
            'allOf': [
                {'$ref': '#/definitions/positionArray'},
                {'minItems': 4}
            ]
        },
        'polygon': {
            'description': 'An array of linear rings',
            'type': 'array',
            'items': {'$ref': '#/definitions/linearRing'}
        }
    }
}, types={'array': (list, tuple)})


def validate_geojson(geometry):
    try:
        geojson_schema.validate(geometry)
    except jsonschema.ValidationError as err:
        raise ValidationError(err.message)
    return geometry


def convert_polygon(geometry):
    geometry = validate_geojson(geometry)
    results = []
    if geometry['type'] == 'Polygon':
        results.append({
            'type': 'Polygon',
            'coordinates': geometry['coordinates']
        })

    elif geometry['type'] == 'MultiPolygon':
        for coords in geometry['coordinates']:
            results.append({
                'type': 'Polygon',
                'coordinates': coords
            })

    return results
