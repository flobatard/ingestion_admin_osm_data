SELECT osm_id, name, admin_level, way, way_area FROM tmp_polygon;

SELECT DISTINCT p2.osm_id, p2.admin_level, p2.name, p1.admin_level 
FROM tmp_polygon p1 
JOIN tmp_polygon p2 ON ST_Contains(p2.way, p1.way) 
WHERE p1.boundary='administrative' AND p2.boundary='administrative' AND p1.osm_id=(%s) AND p1.way=(%s) AND p1.admin_level > p2.admin_level

