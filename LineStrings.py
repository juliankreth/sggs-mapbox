import xml.etree.ElementTree as ET
import json

def parse_coordinates(coordinates_str):
    coordinates = coordinates_str.strip().split()
    parsed_coordinates = []
    for coordinate in coordinates:
        lon, lat, _ = coordinate.split(',')
        parsed_coordinates.append([float(lon), float(lat)])
    return parsed_coordinates

def kml_to_geojson(kml_file, geojson_file):
    tree = ET.parse(kml_file)
    root = tree.getroot()

    features = []
    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name_element = placemark.find('.//{http://www.opengis.net/kml/2.2}name')
        if name_element is not None:
            name = name_element.text
        else:
            name = ''

        coordinates = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates').text

        geometry = {
            'type': 'LineString',
            'coordinates': parse_coordinates(coordinates)
        }

        feature = {
            'type': 'Feature',
            'properties': {'name': name},
            'geometry': geometry
        }

        features.append(feature)

    feature_collection = {
        'type': 'FeatureCollection',
        'features': features
    }

    with open(geojson_file, 'w') as f:
        json.dump(feature_collection, f)

# Aufruf des Skripts
kml_to_geojson('Transpacific.kml', 'Transpacific.geojson')
