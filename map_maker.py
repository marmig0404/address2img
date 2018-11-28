import os

import mapnik
from geographiclib import geodesic, constants
from geopy.geocoders import Nominatim
from mapnik import Box2d

from support import Support


class Map_Maker:
    def __init__(self, addresses, config_file='config.ini'):
        self.addresses = addresses
        self.supporter = Support(config_file)
        self.geolocator = Nominatim(user_agent="AddressConverter")

    def format_address(self, address):
        # Takes address as a string (standard address format)
        # Returns coordinate of address
        location = self.geolocator.geocode(address)
        return location.address

    def convert_address(self, address):
        # Takes address as a string (standard address format)
        # Returns coordinate of address
        location = self.geolocator.geocode(address)
        print(location.address)
        coordinate = [float(location.latitude), float(location.longitude)]
        return coordinate

    @staticmethod
    def get_extents(center, hor_distance, vert_distance):
        # Center as a tuple of latitude and longitude (lat,long)
        # hor_distance is horizontal distance across map in miles
        # vert_distance is vertical distance across map in miles
        # returns a dictionary of tuples, clock wise starting with
        # top left corner
        meters_per_mile = 1609.344
        latitude, longitude = center

        g = geodesic.Geodesic(constants.Constants.WGS84_a, constants.Constants.WGS84_f)

        vert_directions = [0, 180]
        hor_directions = [90, 270]
        distance = {'hor': (hor_distance / 2) * meters_per_mile, 'vert': (vert_distance / 2) * meters_per_mile}

        north_lat = g.Direct(latitude, longitude, vert_directions[0], distance.get('vert'))['lat2']
        south_lat = g.Direct(latitude, longitude, vert_directions[1], distance.get('vert'))['lat2']
        east_lon = g.Direct(latitude, longitude, hor_directions[0], distance.get('hor'))['lon2']
        west_lon = g.Direct(latitude, longitude, hor_directions[1], distance.get('hor'))['lon2']

        extents = Box2d(west_lon, south_lat, east_lon, north_lat)
        return extents

    @staticmethod
    def get_map_name():
        return "map.png"

    def make_map(self):
        # Renders map with mapnik based off stylesheet and settings in config_file

        stylesheet = str(self.supporter.get_config('Map Image Config', 'XML File'))
        width = int(self.supporter.get_config('Map Image Config', 'Width In px'))
        height = int(self.supporter.get_config('Map Image Config', 'Height In px'))

        m = mapnik.Map(width, height)
        mapnik.load_map(m, stylesheet)

        hor_distance = float(self.supporter.get_config('Map Image Config', 'Width In Miles'))
        vert_distance = float(self.supporter.get_config('Map Image Config', 'Height in Miles'))
        image_folder = self.supporter.get_config('Map Image Config', 'Image Directory')

        for address in self.addresses:
            self.supporter.write_to_log("Starting to render map for " + self.format_address(address))
            center = self.convert_address(address)
            extents = self.get_extents(center, hor_distance, vert_distance)
            m.zoom_to_box(extents)

            image_name = self.get_map_name()
            image_location = 'output.png' # str(os.path.join(image_folder, image_name))
            mapnik.render_to_file(m, image_location)
            self.supporter.write_to_log("rendered image to '%s'" % image_location)
