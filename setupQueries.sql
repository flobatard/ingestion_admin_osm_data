CREATE TABLE IF NOT EXISTS public.tmp_polygon
(
    osm_id bigint NOT NULL,
    name text NOT NULL,
    admin_level integer NOT NULL,
    way geometry NOT NULL,
    way_area real NOT NULL,
    boundary text NOT NULL
);

INSERT INTO public.tmp_polygon(
	osm_id, name, admin_level, way, way_area, boundary)
	(SELECT osm_id, name, admin_level, way, way_area, boundary FROM public.planet_osm_polygon WHERE boundary='administrative' AND admin_level IS NOT NULL AND name IS NOT NULL);
	
CREATE INDEX IF NOT EXISTS tmp_polygon_way_idx
    ON public.tmp_polygon USING gist
    (way)
    WITH (FILLFACTOR=100)
;

CREATE INDEX IF NOT EXISTS tmp_polygon_osm_id_index
    ON public.tmp_polygon USING btree
    (osm_id ASC NULLS LAST)
    WITH (FILLFACTOR=100)
;

CREATE INDEX IF NOT EXISTS tmp_polygon_admin_index
    ON public.tmp_polygon USING btree
    (admin_level ASC NULLS LAST)
    WITH (FILLFACTOR=100)