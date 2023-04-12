CREATE INDEX location_naming_osm_id_index
    ON public.location_naming USING btree
    (osm_id ASC NULLS LAST)
    WITH (FILLFACTOR=100)
;

CREATE INDEX location_naming_name_index
    ON public.location_naming USING btree
    (name ASC NULLS LAST)
    WITH (FILLFACTOR=100)
;

CREATE INDEX location_naming_admin_level_index
    ON public.location_naming USING btree
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