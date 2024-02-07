#  Copyright (c) 2024.
#  __author__ = "Dean Hand"
#  __license__ = "AGPL"
#  __version__ = "1.0"

import math
import utm
from pyproj import Transformer, CRS


def decimal_degrees_to_utm(latitude, longitude):
    # Convert decimal degrees to UTM coordinates
    easting, northing, zone, hemisphere = utm.from_latlon(latitude, longitude)
    return easting, northing, zone, hemisphere


def convert_wgs_to_utm(utm_x_str, utm_y_str):
    utm_band = str((math.floor((utm_y_str + 180) / 6) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0'+utm_band
    if utm_x_str >= 0:
        epsg_code = '326' + utm_band
    else:
        epsg_code = '327' + utm_band
    return epsg_code


def utm_to_latlon(utm_x_str, utm_y_str, utm_zone, utm_nth):
    utm_x = utm_x_str
    utm_y = utm_y_str
    lat, lon = utm.to_latlon(utm_x, utm_y, utm_zone, utm_nth)
    return lon, lat


def hemisphere_flag(latitude):
    return 'N' if latitude >= 0 else 'S'


def is_gimbal_pitch_in_range(gimbal_pitch_degree):
    """
    Check if the gimbal pitch degree is within the range of -91 to -89 (inclusive).

    Parameters:
    gimbal_pitch_degree (float): The pitch degree of the gimbal.

    Returns:
    bool: True if within range, False otherwise.
    """
    return -91 <= gimbal_pitch_degree <= -89


def proj_stuff(center_latitude, zone_number):
    # Assuming zone_number and center_latitude are already defined
    is_southern = center_latitude < 0
    utm_crs = CRS(proj='utm', zone=zone_number, ellps='WGS84', datum='WGS84', south=is_southern)
    wgs84_crs = CRS(proj='latlong', datum='WGS84')

    # Initialize the Transformer object for transforming from UTM to WGS84
    transformer = Transformer.from_crs(utm_crs, wgs84_crs, always_xy=True)

    return transformer