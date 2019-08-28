DROP FUNCTION IF EXISTS fuzzy_search(kw varchar);
CREATE or REPLACE FUNCTION fuzzy_search(kw varchar)
    RETURNS TABLE
            (
                city   text,
                county VARCHAR,
                state  VARCHAR,
                id     int4
            )
AS
$$
BEGIN
    RETURN QUERY
        select city_, county_, state_, id_
        from (
                 select null as city_, null as county_, state_name as state_, state_id as id_, 0 as ord
                 from us_states
                 where lower(state_name) like lower(kw)

                 UNION


                 select null as city_, county_name as county_, state_name as state_, con.id_ as id_, 1 as ord
                 from us_states sta,
                      (
                          SELECT county_name, state_id, county_id as id_
                          from us_counties
                          where lower(county_name) like lower(kw)
                      ) as con
                 where con.state_id = sta.state_id

                 union

                 select city_name as city_, county_name as county_, state_name as state_, con.id_ as id_, 2 as ord
                 from us_states sta,
                      (
                          SELECT city_name, county_name, state_id, cit.id_ as id_
                          from us_counties con,
                               (
                                   SELECT city_name, county_id, city_id as id_
                                   from us_cities
                                   where lower(city_name) like lower(kw)
                               ) as cit
                          where cit.county_id = con.county_id
                      ) as con
                 where con.state_id = sta.state_id
             ) as t0
        order by ord

        limit 10;


END;
$$ LANGUAGE plpgsql;


--- usage:
select *
from fuzzy_search('Orange%');
