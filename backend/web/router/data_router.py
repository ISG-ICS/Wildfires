"""
@author: Yuan Fu, Yichi Zhang
"""
import rootpath
rootpath.append()

import json
import os
from typing import List, Dict
from backend.utilities.date_info_series import fill_series, gen_date_series
import matplotlib.path as mplPath
import numpy as np
from flask import Blueprint, make_response, jsonify, send_from_directory, request as flask_request
from backend.connection import Connection
from paths import BOUNDARY_PATH

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route("/aggregation", methods=['POST'])
def aggregation():
    """
    get point-aggregation within a specific radius
    data source is the PRISM table and RECORDS table

    :return:
    """
    request_json = flask_request.get_json(force=True)
    lat = float(request_json['lat'])
    lng = float(request_json['lng'])
    radius = float(request_json['radius'])
    timestamp_str = request_json['timestamp']
    days = int(request_json.get('days', 7))

    # generate date series. values are set to None/null
    date_series = gen_date_series(days, timestamp_str)

    # aggregate_tweet stored procedure, (point_aggr_tweet.sql)
    query_tweet = 'SELECT * from aggregate_tweet(%s, %s, %s, TIMESTAMP %s, %s)'
    query2_tmax = '''
        select rft."date", avg(prism.tmax) from prism,
        (
            SELECT rft."date" from prism_info rft
            where rft."date" <= TIMESTAMP %s -- UTC timezong
            -- returning PDT without timezong label
            and rft."date" > TIMESTAMP %s - ( %s || ' day')::interval
        ) as rft,
        (
            select mesh.gid from us_mesh mesh 
            WHERE st_dwithin(st_makepoint(%s, %s),mesh.geom, %s)
        ) as gids
        where prism.gid=gids.gid
        and prism."date" = rft."date"
        and prism.tmax != FLOAT 'NaN'
        GROUP BY rft."date"
    '''
    query3_vpdmax = '''
        select rft."date", avg(prism.vpdmax) from prism,
        (
            SELECT rft."date" from prism_info rft
            where rft."date" <= TIMESTAMP %s -- UTC timezong
            -- returning PDT without timezong label
            and rft."date" > TIMESTAMP %s - ( %s || ' day')::interval
        ) as rft,
        (
            select mesh.gid from us_mesh mesh 
            WHERE st_dwithin(st_makepoint(%s, %s),mesh.geom, %s)
        ) as gids
        where prism.gid=gids.gid
        and prism."date" = rft."date"
        and prism.vpdmax != FLOAT 'NaN'
        GROUP BY rft."date"
    '''
    query4_ppt = '''
        select rft."date", avg(prism.ppt) from prism,
        (
            SELECT rft."date" from prism_info rft
            where rft."date" <= TIMESTAMP %s -- UTC timezong
            -- returning PDT without timezong label
            and rft."date" > TIMESTAMP %s - ( %s || ' day')::interval
        ) as rft,
        (
            select mesh.gid from us_mesh mesh 
            WHERE st_dwithin(st_makepoint(%s, %s),mesh.geom, %s)
        ) as gids
        where prism.gid=gids.gid
        and prism."date" = rft."date"
        and prism.ppt != FLOAT 'NaN'
        GROUP BY rft."date"
    '''
    with Connection() as conn:
        cur = conn.cursor()

        # tweet count from 'records'
        cur.execute(query_tweet, (lng, lat, radius, timestamp_str, days))  # lng lat +-180
        tweet = cur.fetchall()
        tweet_series = fill_series(date_series, tweet)
        # tmax, vpdmax from PRISM
        cur.execute(query2_tmax, (timestamp_str, timestamp_str, days, lng, lat, radius))
        temp = cur.fetchall()
        temp_series = fill_series(date_series, temp)
        cur.execute(query3_vpdmax, (timestamp_str, timestamp_str, days, lng, lat, radius))
        mois = cur.fetchall()
        mois_series = fill_series(date_series, mois)
        # ppt from PRISM
        cur.execute(query4_ppt, (timestamp_str, timestamp_str, days, lng, lat, radius))
        ppt = cur.fetchall()
        cur.close()
        ppt_series = fill_series(date_series, ppt)
    return make_response(jsonify({'tmp': temp_series, 'soilw': mois_series, 'cnt_tweet': tweet_series,
                                      'ppt': ppt_series}))


@bp.route('region-temp')
def region_temp():
    """
    (unused) average temperature in a administrative boundary
    from NOAA table
    :return:
    """
    region_id = int(flask_request.args.get('region_id'))
    timestamp_str = flask_request.args.get('timestamp')
    days = int(flask_request.args.get('days', 7))

    # generate date series. values are set to None/null
    date_series = gen_date_series(days, timestamp_str)

    query = f'''
    select date(rft.reftime), avg(tmp) from noaa0p25 noaa,
    (
        SELECT reftime, tid from noaa0p25_reftime rft
        where rft.reftime < TIMESTAMP '{timestamp_str}'
        and rft.reftime > TIMESTAMP '{timestamp_str}' - interval '{days} day'
    ) as rft,
    (
        SELECT geometry.gid from noaa0p25_geometry_neg geometry,
        (
            SELECT geom from us_states WHERE state_id={region_id}
            union
            SELECT geom from us_counties WHERE county_id={region_id}
            union
            SELECT geom from us_cities WHERE city_id={region_id}
        ) as region
        where st_contains(region.geom, geometry.geom)
    ) as gids
    where noaa.gid=gids.gid
    and noaa.tid = rft.tid
    GROUP BY date(rft.reftime)
    '''

    return make_response(jsonify(
        fill_series(date_series, Connection.sql_execute(query))))


@bp.route('region-moisture')
def region_moisture():
    """
    (unused) average soil moisture in a administrative boundary
    from NOAA table
    :return:
    """
    region_id = int(flask_request.args.get('region_id'))
    timestamp_str = flask_request.args.get('timestamp')
    days = int(flask_request.args.get('days', 7))

    # generate date series. values are set to None/null
    date_series = gen_date_series(days, timestamp_str)

    query = f'''
    select date(rft.reftime), avg(soilw) from noaa0p25 noaa,
    (
        SELECT reftime, tid from noaa0p25_reftime rft
        where rft.reftime < TIMESTAMP '{timestamp_str}'
        and rft.reftime > TIMESTAMP '{timestamp_str}' - interval '{days} day'
    ) as rft,
    (
        SELECT geometry.gid from noaa0p25_geometry_neg geometry,
        (
            SELECT geom from us_states WHERE state_id={region_id}
            union
            SELECT geom from us_counties WHERE county_id={region_id}
            union
            SELECT geom from us_cities WHERE city_id={region_id}
        ) as region
        where st_contains(region.geom, geometry.geom)
    ) as gids
    where noaa.gid=gids.gid
    and noaa.tid = rft.tid
    GROUP BY date(rft.reftime)
    '''

    return make_response(jsonify(
        fill_series(date_series, Connection.sql_execute(query))))


@bp.route("/temp", methods=['POST'])
def temperature_in_screen():
    """
    (unused) temperature within user screen
    from NOAA table
    :return:
    """
    request_json = flask_request.get_json(force=True)
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']
    tid = request_json['tid']
    interval = request_json['interval']

    query = "SELECT * from Polygon_Aggregator_noaa0p25(%s, %s, %s)"
    poly = 'polygon(({0} {1}, {0} {2}, {3} {2}, {3} {1}, {0} {1}))'.format(north, west, east, south)
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (poly, tid, interval))
        resp = make_response(
            jsonify(
                [{"lon": lon, "lat": lat, "temperature": temp} for lat, lon, temp, _ in cur.fetchall()]))
        cur.close()
    return resp


@bp.route("/soilw", methods=['POST'])
def soil_moisture_in_screen():
    """
    (unused) soil moisture within user screen
    from NOAA table
    :return:
    """

    request_json = flask_request.get_json(force=True)
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']
    tid = request_json['tid']
    interval = request_json['interval']

    query = "SELECT * from Polygon_Aggregator_noaa0p25(%s, %s, %s)"
    poly = 'polygon(({0} {1}, {0} {2}, {3} {2}, {3} {1}, {0} {1}))'.format(north, west, east, south)
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (poly, tid, interval))
        resp = make_response(
            jsonify([{"lon": lon, "lat": lat, "soilw": soilw} for lat, lon, _, soilw in cur.fetchall()]))
        cur.close()
    return resp


@bp.route("/wind")
def wind():
    """
    global wind. from a static file
    :return:
    """
    # TODO: replace source of wind data to db
    return make_response(send_from_directory('static/data', 'latest.json'))


@bp.route("/rain_fall")
def rainfall():
    """
    (unused) rain fall data from a static .csv file
    """
    # TODO: replace source of rain fall data to db
    return make_response(send_from_directory('data', 'rain_fall_sample.csv'))


@bp.route("/recent-temp")
def send_temperature_data():
    """
        This func gives the second lastest data for temperature within ractangle around US,
        since the most lastest data is always updating (not completed)

        :returns: a list of temp objects, with lat, long, and temp value
    """
    temperature_fetch = Connection.sql_execute("select t.lat, t.long, t.temperature from recent_temperature t "
                                                 "where t.endtime = (select max(t.endtime) from recent_temperature t"
                                                 " where t.endtime <(select max(t.endtime) from recent_temperature t))")

    temperature_data_celsius = []  # format temp data into a dictionary structure

    for row in temperature_fetch:
        temperature_object = {
            "lat": row[0],
            "long": row[1] % (-360),  # convert longtitude range
            "temp": row[2] - 273.15,  # change temp into celsius
        }

        temperature_data_celsius.append(temperature_object)

    temperature_data_us = points_in_us(temperature_data_celsius)  # restrict data within US boundary.

    resp = make_response(jsonify(temperature_data_us))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # sends temperature data with coordinate within us boundary
    return resp


def points_in_us(pnts: List[Dict[str, float]], accuracy=0.001):
    """
        To filter a list of points dict to a list of them within us boundary
        :param pnts: list of raw points that to be filtered. The format is [{lng: .., lat: .., else: ..}, ...]
        :param accuracy: Allow the path to be made slightly larger or smaller by change the default set of this value.
        :returns: a list of filtered points, in the same format of input pnt dicts
    """
    if not isinstance(pnts, list):
        raise TypeError("Input should be list as : [dict, dict, ...]")

    # TODO: move this bound file to database.
    with open(os.path.join(BOUNDARY_PATH, "USbound.json")) as json_file:
        data = json.load(json_file)
        main_land_poly = mplPath.Path(np.array(data["mainland"][::5]))
        result = []
        for pnt in pnts:
            if main_land_poly.contains_point([pnt['long'] % -360, pnt['lat']], radius=accuracy) \
                    or main_land_poly.contains_point([pnt['long'] % -360, pnt['lat']], radius=-accuracy):
                result.append(pnt)
        return result


@bp.route("/fire-polygon", methods=['POST'])
def fire():
    # return a json of all fire name, fire time, and fire geometry inside the bounding box
    request_json = flask_request.get_json(force=True)
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']
    size = request_json['size']
    start_date = request_json['startDate'][:10]
    end_date = request_json['endDate'][:10]
    size_getters = {0: "geom_full", 1: "geom_1e4", 2: "geom_1e3", 3: "geom_1e2",
                    4: "geom_center"}
    poly = 'polygon(({0} {1}, {0} {2}, {3} {2}, {3} {1}, {0} {1}))'.format(east, south, north, west)
    query = f"SELECT id, name, agency,start_time, end_time, st_asgeojson({size_getters[size]}) as geom, max_area FROM " \
            f"fire_merged f WHERE ((('{start_date}'::date <= f.end_time::date) AND " \
            f"('{start_date}'::date >= f.start_time::date)) OR (('{end_date}'::date >= f.start_time::date) " \
            f"AND ('{end_date}'::date <= f.end_time::date)) OR (('{start_date}'::date <= f.start_time::date) " \
            f"AND ('{end_date}'::date >= f.end_time::date) )) " \
            f"AND (st_contains(ST_GeomFromText('{poly}'),f.{size_getters[size]}) " \
            f"OR st_overlaps(ST_GeomFromText('{poly}'),f.{size_getters[size]}))"
    return make_response(jsonify([{"type": "Feature",
                                   "id": fid,
                                   "properties": {"name": name, "agency": agency, "starttime": start_time,
                                                  "endtime": end_time, "density": 520, "area": max_area},
                                   "geometry": json.loads(geom)}
                                  for fid, name, agency, start_time, end_time, geom, max_area
                                  in Connection.sql_execute(query)]))


@bp.route("/fire-with-id", methods=['POST'])
def fire_with_id():
    request_json = flask_request.get_json(force=True)
    id = request_json['id']
    size = request_json['size']
    size_getters = {0: "geom_full", 1: "geom_1e4", 2: "geom_1e3", 3: "geom_1e2",
                    4: "geom_center"}
    query = f"SELECT " \
            f"id, name, if_sequence, agency, state, start_time, end_time, st_asgeojson({size_getters[size]}) as geom," \
            f" st_asgeojson(st_envelope({size_getters[size]})) as bbox, " \
            f"max_area FROM fire_merged where id = {id}"
    return make_response(jsonify([{"type": "Feature",
                                   "id": fid,
                                   "properties": {"name": name, "agency": agency, "if_sequence": if_sequence,
                                                  "starttime": start_time,
                                                  "endtime": end_time, "density": 520, "area": max_area,
                                                  "state": state},
                                   "geometry": json.loads(geom),
                                   "bbox": json.loads(bbox)
                                   }
                                  for fid, name, if_sequence, agency, state, start_time, end_time, geom, bbox, max_area
                                  in Connection.sql_execute(query)]))


@bp.route("/fire-with-id-seperated", methods=['POST'])
def fire_with_id_seperated():
    request_json = flask_request.get_json(force=True)
    id = request_json['id']
    size = request_json['size']
    size_getters = {0: "geom_full", 1: "geom_1e4", 2: "geom_1e3", 3: "geom_1e2",
                    4: "geom_center"}
    query = f"SELECT " \
            f"f.id, f.name, f.if_sequence, f.agency, f.state, f.time,st_asgeojson(f.{size_getters[size]}) as geom," \
            f" st_asgeojson(st_envelope(m.{size_getters[size]})) as bbox," \
            f" f.area FROM fire_merged m, fire f where f.id = {id} and m.id = f.id"
    return make_response(jsonify([{"type": "Feature",
                                   "id": fid,
                                   "properties": {"name": name, "agency": agency, "if_sequence": if_sequence,
                                                  "time": time,
                                                  "density": 520, "area": max_area, "state": state},
                                   "geometry": json.loads(geom),
                                   "bbox": json.loads(bbox)
                                   }
                                  for fid, name, if_sequence, agency, state, time, geom, bbox, max_area
                                  in Connection.sql_execute(query)]))
