CREATE TABLE public.location_naming
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    osm_id bigint NOT NULL,
    name text NOT NULL,
    admin_level integer NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT osm_id_unique UNIQUE (osm_id)
);

CREATE TABLE public.location
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    level_1 bigint DEFAULT NULL,
    level_2 bigint DEFAULT NULL,
    level_3 bigint DEFAULT NULL,
    level_4 bigint DEFAULT NULL,
    level_5 bigint DEFAULT NULL,
    level_6 bigint DEFAULT NULL,
    level_7 bigint DEFAULT NULL,
    level_8 bigint DEFAULT NULL,
    level_9 bigint DEFAULT NULL,
    level_10 bigint DEFAULT NULL,
    level_11 bigint DEFAULT NULL,
    level_12 bigint DEFAULT NULL,
    level_13 bigint DEFAULT NULL,
    level_14 bigint DEFAULT NULL,
    level_15 bigint DEFAULT NULL,
    admin_level integer NOT NULL,
    way geometry NOT NULL,
    osm_id bigint NOT NULL,
    name text NOT NULL,
    way_area real NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT osm_id_level_1 FOREIGN KEY (level_1)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_2 FOREIGN KEY (level_2)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_3 FOREIGN KEY (level_3)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_4 FOREIGN KEY (level_4)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_5 FOREIGN KEY (level_5)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_6 FOREIGN KEY (level_6)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_7 FOREIGN KEY (level_7)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_8 FOREIGN KEY (level_8)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_9 FOREIGN KEY (level_9)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_10 FOREIGN KEY (level_10)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_11 FOREIGN KEY (level_11)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_12 FOREIGN KEY (level_12)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_13 FOREIGN KEY (level_13)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_14 FOREIGN KEY (level_14)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT osm_id_level_15 FOREIGN KEY (level_15)
        REFERENCES public.location_naming (osm_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);