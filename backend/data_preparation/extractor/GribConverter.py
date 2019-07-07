import pygrib
import numpy as np


class GribConverter:
    @staticmethod
    def convert(filepath):
        grbs = pygrib.open(filepath)
        result_list = list()
        result = {'header': dict(), 'data': np.array(list())}
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
            result = {'header': dict(), 'data': list()}
        return result_list
