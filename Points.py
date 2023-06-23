import xml.etree.ElementTree as ET
import json

def kml_to_geojson(kml_file, output_file):
    # KML-Namespace definieren
    ns = {"ns0": "http://www.opengis.net/kml/2.2"}

    # XML-Elementbaum aus der KML-Datei erstellen
    tree = ET.parse(kml_file)
    root = tree.getroot()

    # GeoJSON-Feature-Collection erstellen
    features = []
    for placemark in root.findall(".//ns0:Placemark", ns):
        name = placemark.find("ns0:name", ns).text
        description = placemark.find("ns0:description", ns).text
        coordinates = placemark.find("ns0:Point/ns0:coordinates", ns).text

        # Koordinaten aufteilen und umkehren
        longitude, latitude, altitude = map(float, coordinates.split(","))
        coordinates = [longitude, latitude]

        # GeoJSON-Feature erstellen
        feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "description": description
            },
            "geometry": {
                "type": "Point",
                "coordinates": coordinates
            }
        }

        features.append(feature)

    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }

    # GeoJSON als JSON-String konvertieren
    geojson = json.dumps(feature_collection, indent=2)

    # GeoJSON in eine Datei speichern
    with open(output_file, "w") as file:
        file.write(geojson)

# KML-Datei in GeoJSON konvertieren und speichern
kml_file = "US_Sites.kml"
output_file = "US_Sites.geojson"
kml_to_geojson(kml_file, output_file)

print("Konvertierung abgeschlossen. Das GeoJSON wurde in '{}' gespeichert.".format(output_file))
