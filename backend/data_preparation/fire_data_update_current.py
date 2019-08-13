from backend.data_preparation.connection import Connection
import datetime
sql_check_if_fire_aggregate_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_aggregated\''

sql_create_new_table = "CREATE TABLE IF NOT EXISTS fire_aggregated (name varchar(40), agency text, if_sequence boolean, " \
                       "geom_full geometry, geom_1e4 geometry, geom_1e3 geometry, geom_1e2 geometry, center geometry, start_time timestamp," \
                       "end_time timestamp, PRIMARY KEY (name, start_time, end_time))"

sql_get_all_fire_names = "select distinct (name) from fire_info_1;"

sql_get_fire_with_name = "select * from fire_info_1 where name = %s"

sql_insert_record = "INSERT INTO fire_aggregated (name, agency, if_sequence, geom_full, geom_1e4, geom_1e3, geom_1e2, center, start_time, end_time) VALUES ('{name}', '{agency}', {if_seq}, {geom_f},{geom_4}, {geom_3}, {geom_2},st_centroid({center}), '{st}', '{et}')"



def create_table(conn):
    cur = conn.cursor()
    cur.execute(sql_check_if_fire_aggregate_table_exists)
    tables = cur.fetchall()
    if len(tables) == 0:
        print("No history table exists. Creating a new one.")
        cur.execute(sql_create_new_table)
        conn.commit()
    cur.close()


def retrieve_all_fire_names(conn):
    cur = conn.cursor()
    cur.execute(sql_get_all_fire_names)
    result = cur.fetchall()
    cur.close()
    return result


def retrieve_data_of_a_fire(conn, firename):
    cur = conn.cursor()
    cur.execute(sql_get_fire_with_name, firename)
    result = cur.fetchall()
    cur.close()
    return result


def get_full_fire_period(firelist:list):
    start_time = firelist[0][3]
    end_time = firelist[0][3]
    for f in firelist:
        if start_time > f[3]:
            start_time = f[3]
        if end_time < f[3]:
            end_time = f[3]
    return end_time, start_time

def get_aggregated_agency(current_fire):
    result = ""
    for f in current_fire:
        if not f[2] in result:
            result += ", " + f[2]
    return result[2:]

def polygons_to_string(polygons):
    result ="ST_AsText(ST_Union(ARRAY["
    for p in polygons:
        result += f"st_makevalid(ST_GeomFromText(ST_ASTEXT('{p}'))),"
    result = result[:-1] + "]) )"
    return result

def insert_one_fire_merged(current_fire):
    name = current_fire[0][0]
    if_sequence = current_fire[0][1]
    agency = get_aggregated_agency(current_fire)
    end_time, start_time = get_full_fire_period(current_fire)
    polygons_full = [f[4] for f in current_fire]
    geom_full = polygons_to_string(polygons_full)
    polygons_1e4 = [f[5] for f in current_fire]
    geom_1e4 = polygons_to_string(polygons_1e4)
    polygons_1e3 = [f[6] for f in current_fire]
    geom_1e3 = polygons_to_string(polygons_1e3)
    polygons_1e2 = [f[7] for f in current_fire]
    geom_1e2 = polygons_to_string(polygons_1e2)
    center = [f[8] for f in current_fire]
    geom_center = polygons_to_string(center)
    return sql_insert_record.format(name=name,agency=agency,if_seq=if_sequence,et=end_time,st=start_time,geom_f=geom_full,geom_4=geom_1e4,geom_3=geom_1e3,geom_2=geom_1e2,center=geom_center)

def exec_insert(current_fire,conn):
    cur = conn.cursor()
    cur.execute(insert_one_fire_merged(current_fire))
    conn.commit()
    cur.close()

with Connection() as conn:
    create_table(conn)
    list_of_fire_names = retrieve_all_fire_names(conn)
    print(list_of_fire_names)

    for name in list_of_fire_names:
        fire_with_the_name = []
        all_records_of_fire = retrieve_data_of_a_fire(conn, name)
        end_time, start_time = get_full_fire_period(all_records_of_fire)
        time_period = end_time - start_time
        pause_limit = time_period * 0.8
        current_fire = []
        time = all_records_of_fire[0][3]
        for record in all_records_of_fire:
            if record[3] - time > pause_limit:
                print(insert_one_fire_merged(current_fire))
                exec_insert(current_fire,conn)
                current_fire = list()
                current_fire.append(record)
            else:
                current_fire.append(record)
            time = record[3]
        exec_insert(current_fire,conn)






