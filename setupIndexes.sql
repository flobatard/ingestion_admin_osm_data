CREATE INDEX naming_location_osm_id_index
    ON public.naming_location USING btree
    (osm_id ASC NULLS LAST)
    WITH (FILLFACTOR=100)
;

CREATE INDEX naming_location_name_index
    ON public.naming_location USING btree
    (name ASC NULLS LAST)
    WITH (FILLFACTOR=100)
;

CREATE INDEX naming_location_admin_level_index
    ON public.naming_location USING btree
    (admin_level ASC NULLS LAST)
    WITH (FILLFACTOR=100)
;

CREATE INDEX location_way_index
    ON public.location USING gist
    (way)
    WITH (FILLFACTOR=100)
;

CREATE INDEX location_level_$1_index
    ON public.location USING btree
    (level_$1)
    WITH (FILLFACTOR=100)
;

CREATE INDEX location_osm_id_index
    ON public.location USING btree
    (osm_id)
    WITH (FILLFACTOR=100)
;

CREATE INDEX location_admin_level_index
    ON public.location USING btree
    (admin_level)
    WITH (FILLFACTOR=100)
;

CREATE INDEX location_name_index
    ON public.location USING btree
    (name)
    WITH (FILLFACTOR=100)
;