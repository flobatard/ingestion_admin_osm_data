SELECT DISTINCT osm_id, name, admin_level 
FROM public.tmp_polygon
WHERE boundary='administrative' AND admin_level IS NOT NULL AND name IS NOT NULL;

INSERT INTO public.naming_location(osm_id, name, admin_level) 
VALUES (%s, %s, %s) 
