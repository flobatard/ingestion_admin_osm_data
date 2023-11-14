SELECT DISTINCT osm_id, name, admin_level 
FROM public.tmp_polygon
WHERE boundary='administrative' AND admin_level IS NOT NULL AND name IS NOT NULL;

INSERT INTO public.location_naming(osm_id, name, admin_level) 
VALUES (%(osm_id)s, %(name)s, %(admin_level)s) 
ON CONFLICT (osm_id)
DO 
    UPDATE SET name=%(name)s, admin_level=%(admin_level)s WHERE location_naming.osm_id=%(osm_id)s
