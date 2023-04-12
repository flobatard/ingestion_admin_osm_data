SELECT DISTINCT  
l.osm_id, l.name, l.admin_level,
to_tsvector(
COALESCE (l1.name || ',', '') ||  
COALESCE (l2.name || ',', '') ||
COALESCE (l3.name || ',', '') ||
COALESCE (l4.name || ',', '') ||
COALESCE (l5.name || ',', '') ||  
COALESCE (l6.name || ',', '') ||
COALESCE (l7.name || ',', '') ||
COALESCE (l8.name || ',', '') ||
COALESCE (l9.name || ',', '') ||  
COALESCE (l10.name || ',', '') ||
COALESCE (l11.name || ',', '') ||
COALESCE (l12.name || ',', '') ||
COALESCE (l13.name || ',', '') ||  
COALESCE (l14.name || ',', '') ||
COALESCE (l15.name || ',', '') ) as ts
COALESCE (l1.name || ',', '') ||  
COALESCE (l2.name || ',', '') ||
COALESCE (l3.name || ',', '') ||
COALESCE (l4.name || ',', '') ||
COALESCE (l5.name || ',', '') ||  
COALESCE (l6.name || ',', '') ||
COALESCE (l7.name || ',', '') ||
COALESCE (l8.name || ',', '') ||
COALESCE (l9.name || ',', '') ||  
COALESCE (l10.name || ',', '') ||
COALESCE (l11.name || ',', '') ||
COALESCE (l12.name || ',', '') ||
COALESCE (l13.name || ',', '') ||  
COALESCE (l14.name || ',', '') ||
COALESCE (l15.name || ',', '') ) as complete_string

INTO search_location
FROM location as l
LEFT JOIN location_naming as l1 ON l1.osm_id=level_1
LEFT JOIN location_naming as l2 ON l2.osm_id=level_2
LEFT JOIN location_naming as l3 ON l3.osm_id=level_3
LEFT JOIN location_naming as l4 ON l4.osm_id=level_4
LEFT JOIN location_naming as l5 ON l5.osm_id=level_5
LEFT JOIN location_naming as l6 ON l6.osm_id=level_6
LEFT JOIN location_naming as l7 ON l7.osm_id=level_7
LEFT JOIN location_naming as l8 ON l8.osm_id=level_8
LEFT JOIN location_naming as l9 ON l9.osm_id=level_9
LEFT JOIN location_naming as l10 ON l10.osm_id=level_10
LEFT JOIN location_naming as l11 ON l11.osm_id=level_11
LEFT JOIN location_naming as l12 ON l12.osm_id=level_12
LEFT JOIN location_naming as l13 ON l13.osm_id=level_13
LEFT JOIN location_naming as l14 ON l14.osm_id=level_14
LEFT JOIN location_naming as l15 ON l15.osm_id=level_15
ORDER BY admin_level;

CREATE INDEX ts_idx ON search_location USING GIN (ts);