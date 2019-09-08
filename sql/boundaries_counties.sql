DROP FUNCTION IF EXISTS boundaries_counties(poly VARCHAR);
CREATE or REPLACE FUNCTION boundaries_counties(poly VARCHAR)
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
        SELECT county_id, county_name, ST_AsGeoJSON(geom)
        from us_counties
        where ST_intersects(geom, ST_GeomFromText(poly));

END;
$$ LANGUAGE plpgsql;

-- usage: lon lat, +-180
SELECT *
from boundaries_counties('polygon((-120 20, -100 20, -100 40, -120 40, -120 20))');
