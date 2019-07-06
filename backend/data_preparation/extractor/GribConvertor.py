import json
import pygrib
import numpy as np


class GribConvertor:
    @staticmethod
    def convert(filepath):
        grbs = pygrib.open(filepath)
        grbs.seek(0)
        result_list = []
        result = {}
        result['header'] = {}
        result['data'] = np.array([])
        for g in grbs:
            for row in g['values']:
                result['data'] = np.concatenate((result['data'], row), axis=0)
            result['header'] = {
                'parameterCategory': g["parameterCategory"],
                'parameterNumber': g['parameterNumber'],
                'numberPoints': len(result['data']),
                'nx': g['Ni'],
                'ny': g['Nj'],
                'lo1': g['longitudeOfFirstGridPointInDegrees'],
                'lo2': g['longitudeOfLastGridPointInDegrees'],
                'la1': g['latitudeOfFirstGridPointInDegrees'],
                'la2': g['latitudeOfLastGridPointInDegrees'],
                'dx': g['iDirectionIncrementInDegrees'],
                'dy': g['jDirectionIncrementInDegrees'],
            }
            result['data'] = result['data'].tolist()
            result_list.append(result)
            result = {}
            result['header'] = {}
            result['data'] = []
        return result_list
