# AddressConverter.py
# GroupGolfer Map Image Generator
# October 2018

from geopy.geocoders import Nominatim


def convert_address(address):
    geolocator = Nominatim(user_agent="AddressConverter")
    location = geolocator.geocode(address)
    coordinate = [location.latitude, location.longitude]
    return coordinate


def convert_addresses(addresses):
    coordinates = []
    length = len(addresses)
    index = 0
    while index < length:
        address = addresses[index]
        coordinates.append(convert_address(address))
        index += 1
    return coordinates
