from geographiclib import geodesic, constants

meters_per_mile = 1609.344


def get_extents(center, hor_distance, vert_distance):
    # Center as a tuple of latitude and longitude (lat,long)
    # hor_distance is horizontal distance from center in miles
    # vert_distance is vertical distance from center in miles
    # returns a dictionary of tuples, clock wise starting with
    # top left corner

    latitude, longitude = center

    g = geodesic.Geodesic(constants.Constants.WGS84_a, constants.Constants.WGS84_f)

    vert_directions = [0, 180]
    hor_directions = [90, 270]
    distance = {'hor': hor_distance * meters_per_mile, 'vert': vert_distance * meters_per_mile}

    north_lat = g.Direct(latitude, longitude, vert_directions[0], distance.get('vert'))['lat2']
    south_lat = g.Direct(latitude, longitude, vert_directions[1], distance.get('vert'))['lat2']
    east_lon = g.Direct(latitude, longitude, hor_directions[0], distance.get('hor'))['lon2']
    west_lon = g.Direct(latitude, longitude, hor_directions[1], distance.get('hor'))['lon2']

    extents = dict({'top_left': (north_lat, west_lon),
                    'top_right': (north_lat, east_lon),
                    'bottom_right': (south_lat, east_lon),
                    'bottom_left': (south_lat, west_lon),
                    })
    return extents
