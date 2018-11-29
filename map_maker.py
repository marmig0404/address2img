import os
import time

import mapnik
from geographiclib import geodesic, constants
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from mapnik import Box2d

from support import Support, start_time


class Map_Maker:

    def __init__(self, addresses, config_file='config.ini'):
        self.addresses = addresses
        self.number_of_addresses = len(addresses)
        self.number_of_rendered = 0
        self.supporter = Support(config_file)
        self.supporter.write_to_log('Address2img Initialized.')
        self.supporter.write_to_log('Rendering maps for %s location(s)' % self.number_of_addresses)

    @staticmethod
    def get_geolocator(hash_data):
        return Nominatim(user_agent=str(hash(hash_data)))

    @staticmethod
    def format_address(geocoder, address):
        # Takes address as a string (standard address format)
        # Returns coordinate of address
        location = geocoder.geocode(address)
        formatted_address = location.address
        return formatted_address

    @staticmethod
    def convert_address(geocoder, address):
        # Takes address as a string (standard address format)
        # Returns coordinate of address
        location = geocoder.geocode(address)
        coordinate = [float(location.latitude), float(location.longitude)]
        return coordinate

    def check_address(self, address):

        timed_out = False
        while not timed_out:
            try:
                geocoder = self.get_geolocator('address2img:check' + address)
                test = geocoder.geocode(address).address
                del test
                return True, geocoder
            except GeocoderTimedOut:
                self.supporter.write_to_log("Timed out, trying to connect again")
                time.sleep(int(self.supporter.get_config('General Config', 'Geopy Timeout')))
                timed_out = True
            except AttributeError:
                self.supporter.write_to_log("Skipping invalid address: " + address)
                self.supporter.write_to_log("Location does not exist or is formatted incorrectly.")
                return False, None

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

    def get_map_name(self, address):

        file_type = self.supporter.get_config('Map Image Config', 'Output File Type')
        image_hash = str(hash(address))[-6:]
        image_folder = self.supporter.get_config('Map Image Config', 'Image Directory')
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        image_location = os.path.join(image_folder, ('map-' + image_hash + '.' + file_type))
        return image_location

    def rename_map(self, original_map, address):
        image_name = self.get_map_name(address)
        os.rename(original_map, image_name)
        return image_name

    def make_map(self):
        # Renders map with mapnik based off stylesheet and settings in config_file
        temp_dir = str(self.supporter.get_config('General Config', 'Temporary Directory'))
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        temp_map = os.path.join(temp_dir, 'temp.png')

        stylesheet = str(self.supporter.get_config('Map Image Config', 'XML File'))
        width = int(self.supporter.get_config('Map Image Config', 'Width In px'))
        height = int(self.supporter.get_config('Map Image Config', 'Height In px'))

        m = mapnik.Map(width, height)
        mapnik.load_map(m, stylesheet)

        hor_distance = float(self.supporter.get_config('Map Image Config', 'Width In Miles'))
        vert_distance = float(self.supporter.get_config('Map Image Config', 'Height in Miles'))

        for count, address in enumerate(self.addresses):
            address = str(address.encode('utf-8'))
            address_is_good = self.check_address(address)[0]
            if address_is_good:
                geocoder = self.check_address(address)[1]
                self.supporter.write_to_log("(%s/%s) Starting to render map for %s" %
                                            (self.number_of_addresses,
                                             count,
                                             self.format_address(geocoder, address)))
                center = self.convert_address(geocoder, address)
                extents = self.get_extents(center, hor_distance, vert_distance)
                m.zoom_to_box(extents)
                mapnik.render_to_file(m, temp_map)
                image_name = self.rename_map(temp_map, address)
                self.supporter.write_to_log("(%s/%s) Rendered map to '%s' for '%s'" %
                                            (count,
                                             self.number_of_addresses,
                                             image_name,
                                             self.format_address(geocoder, address)))
                self.number_of_rendered = self.number_of_rendered + 1

    def __del__(self):
        end_time = time.time()
        time_to_render = round(end_time - start_time, 2)
        self.supporter.write_to_log("Rendered %s maps for %s location(s) in %s seconds." % (self.number_of_rendered,
                                                                                            self.number_of_addresses,
                                                                                            time_to_render))
