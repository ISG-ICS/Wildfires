DROP FUNCTION IF EXISTS boundaries_states(poly VARCHAR);
CREATE or REPLACE FUNCTION boundaries_states(poly VARCHAR)
    RETURNS TABLE
            (
                id      int,
                name    varchar,
                geojson text
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT state_id, state_name, ST_AsGeoJSON(geom)
        from us_states
        where ST_intersects(geom, ST_GeomFromText(poly));

END;
$$ LANGUAGE plpgsql;

-- usage: lon lat, +-180
SELECT *
from boundaries_states('polygon((-120 20, -100 20, -100 40, -120 40, -120 20))');
