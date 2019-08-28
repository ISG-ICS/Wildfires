DROP FUNCTION IF EXISTS aggregate_tweet(long FLOAT, lat FLOAT, radius FLOAT, stamp TIMESTAMP, days int);
CREATE or REPLACE FUNCTION aggregate_tweet(long FLOAT, lat FLOAT, radius FLOAT, stamp TIMESTAMP, days int)
    RETURNS TABLE
            (
                timeref   date,
                cnt_tweet bigint
            )
AS
$$
BEGIN
    RETURN QUERY
        select date(rft.create_at), count(t.id)
        from locations t,
             (
                 SELECT create_at, id
                 from records rft
                 where create_at < stamp -- UTC timezong
                   -- returning PDT without timezong label
                   and create_at > stamp - (days || ' day')::interval
             ) as rft
        WHERE st_dwithin(st_makepoint(long, lat), st_makepoint(t.top_left_long, t.top_left_lat), radius)
          and rft."id" = t."id"
        GROUP BY date(rft.create_at);

END;
$$
    LANGUAGE 'plpgsql';

-- usage: lon lat +-180
SELECT *
from aggregate_tweet(-74.026675, 40.683935, 5, TIMESTAMP '2019-08-06T15:37:27Z', 7);
