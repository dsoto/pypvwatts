# coding: utf-8
"""
Python wrapper for NREL PVWatt version 4.
"""
from .pvwattsresult import PVWattsResult
from .pvwattserror import PVWattsError, PVWattsValidationError
import requests
from .__version__ import VERSION

import sys

import functools

if sys.version_info >= (3, 0):
    numerical_types = (int, float)
    numerical_str = ' must be int or float'
    str_types = (str)
    str_str = ' must be str'
elif sys.version_info <= (3, 0):
    numerical_types = (int, long, float)
    numerical_str = ' must be int, long, or float'
    str_types = (str, unicode)
    str_str = ' must be str or unicode'

# this decorator lets me use methods as both static and instance methods
class omnimethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return functools.partial(self.func, instance)


class PVWatts():
    '''
    A Python wrapper for NREL PVWatts V4.0.0 API
    '''

    PVWATTS_QUERY_URL = 'http://developer.nrel.gov/api/pvwatts/v4.json'
    api_key = 'DEMO_KEY'


    def __init__(self, api_key='DEMO_KEY', proxies=None):
        PVWatts.api_key = api_key
        self.proxies = proxies

    @omnimethod
    def validate_system_size(self, system_size):
        if system_size is None:
            return

        #if not isinstance(system_size, (int, long, float)):
        if not isinstance(system_size, numerical_types):
            raise PVWattsValidationError('system_size' + numerical_str)

        if not (0.05 <= system_size and system_size <= 500000):
            raise PVWattsValidationError('system_size must be >= 0.05 and <= 500000')

        return system_size

    @omnimethod
    def validate_lat(self, lat):
        if lat is None:
            return

        if not isinstance(lat, numerical_types):
            raise PVWattsValidationError('lat' + numerical_str)

        if not (-90 <= lat and lat <= 90):
            raise PVWattsValidationError('lat must be >= -90 and <= 90')

        return lat

    @omnimethod
    def validate_lon(self, lon):
        if lon is None:
            return

        if not isinstance(lon, numerical_types):
            raise PVWattsValidationError('lon' + numerical_str)

        if not (-180 <= lon and lon <= 180):
            raise PVWattsValidationError('lon must be >= -90 and <= 90')

        return lon

    @omnimethod
    def validate_dataset(self, dataset):
        if dataset is None:
            return

        if not isinstance(dataset, str_types):
            raise PVWattsValidationError('dataset' + str_str)

        if dataset not in ('tmy2', 'tmy3', 'intl'):
            raise PVWattsValidationError('dataset must be \'tmy2\', \'tmy3\' or \'intl\'')

        return dataset

    @omnimethod
    def validate_timeframe(self, timeframe):
        if timeframe is None:
            return

        if not isinstance(timeframe, str_types):
            raise PVWattsValidationError('timeframe' + str_str)

        if timeframe not in ('hourly', 'monthly'):
            raise PVWattsValidationError('dataset must be \'hourly\' or \'monthly\'')

        return timeframe

    @omnimethod
    def validate_azimuth(self, azimuth):
        if azimuth is None:
            return

        if not isinstance(azimuth, numerical_types):
            raise PVWattsValidationError('azimuth' + numerical_str)

        if not (0 <= azimuth and azimuth <= 360):
            raise PVWattsValidationError('azimuth must be >= 0 and <= 360')

        return azimuth

    @omnimethod
    def validate_derate(self, derate):
        if derate is None:
            return

        if not isinstance(derate, numerical_types):
            raise PVWattsValidationError('derate' + numerical_str)

        if not (0 <= derate and derate <= 1):
            raise PVWattsValidationError('derate must be >= 0 and <= 1')

        return derate

    @omnimethod
    def validate_tilt(self, tilt):
        if tilt is None:
            return

        if not isinstance(tilt, numerical_types):
            raise PVWattsValidationError('tilt' + numerical_str)

        return tilt

    @omnimethod
    def validate_tilt_eq_lat(self, tilt_eq_lat):
        if tilt_eq_lat is None:
            return

        if not isinstance(tilt_eq_lat, numerical_types):
            raise PVWattsValidationError('tilt_eq_lat' + numerical_str)
        if tilt_eq_lat not in (0, 1):
            raise PVWattsValidationError('tilt_eq_lat must be 0 or 1')

        return tilt_eq_lat

    @omnimethod
    def validate_track_mode(self, track_mode):
        if track_mode is None:
            return

        if not isinstance(track_mode, numerical_types):
            raise PVWattsValidationError('track_mode' + numerical_str)

        if track_mode not in (0, 1, 2):
            raise PVWattsValidationError('track_mode must be 0, 1 or 2')

        return track_mode

    @omnimethod
    def validate_inoct(self, inoct):
        if inoct is None:
            return

        if not isinstance(inoct, numerical_types):
            raise PVWattsValidationError('inoct' + numerical_str)

        if not (30 <= inoct and inoct <= 80):
            raise PVWattsValidationError('inoct must be >= 30 and <= 80')

        return inoct

    @omnimethod
    def validate_gamma(self, gamma):
        if gamma is None:
            return

        if not isinstance(gamma, numerical_types):
            raise PVWattsValidationError('gamma' + numerical_str)

        if not (-2 <= gamma and gamma <= -0.01):
            raise PVWattsValidationError('gamma must be >= -2 and <= -0.01')

        return gamma

    @property
    def version(self):
        return VERSION

    @omnimethod
    def get_data(self, params={}):
        """
        Make the request and return the deserialided JSON from the response

        :param params: Dictionary mapping (string) query parameters to values
        :type params: dict
        :return: JSON object with the data fetched from that URL as a
                 JSON-format object.
        :rtype: (dict or array)

        """
        if self and hasattr(self, 'proxies') and self.proxies is not None:
            response = requests.request('GET',
                                        url=PVWatts.PVWATTS_QUERY_URL,
                                        params=params,
                                        headers={'User-Agent': ''.join(
                                                 ['pypvwatts/', VERSION,
                                                  ' (Python)'])},
                                        proxies=self.proxies)
        else:
            response = requests.request('GET',
                                        url=PVWatts.PVWATTS_QUERY_URL,
                                        params=params,
                                        headers={'User-Agent': ''.join(
                                                 ['pypvwatts/', VERSION,
                                                  ' (Python)'])})

        if response.status_code == 403:
            raise PVWattsError("Forbidden, 403")
        return response.json()

    @omnimethod
    def request(self, format=None, system_size=None, address=None, lat=None,
                lon=None, file_id=None, dataset='tmy3', timeframe='monthly',
                azimuth=None, derate=None, tilt=None, tilt_eq_lat=0,
                track_mode=1, inoct=None, gamma=None, callback=None):

        params = {'format': format,
                  'system_size': PVWatts.validate_system_size(system_size),
                  'address': address,
                  'lat': PVWatts.validate_lat(lat),
                  'lon': PVWatts.validate_lon(lon),
                  'file_id': file_id,
                  'dataset': PVWatts.validate_dataset(dataset),
                  'timeframe': PVWatts.validate_timeframe(timeframe),
                  'azimuth': PVWatts.validate_azimuth(azimuth),
                  'derate': PVWatts.validate_derate(derate),
                  'tilt': PVWatts.validate_tilt(tilt),
                  'tilt_eq_lat': PVWatts.validate_tilt_eq_lat(tilt_eq_lat),
                  'track_mode': PVWatts.validate_track_mode(track_mode),
                  'inoct': PVWatts.validate_inoct(inoct),
                  'gamma': PVWatts.validate_gamma(gamma),
                  'callback': callback}

        params['api_key'] = PVWatts.api_key

        if self is not None:
            return PVWattsResult(self.get_data(params=params))
        return PVWattsResult(PVWatts.get_data(params=params))
