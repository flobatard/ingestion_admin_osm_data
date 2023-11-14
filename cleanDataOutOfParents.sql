SELECT 
COUNT(osm_id), sub.name, sub.admin_level, osm_id
FROM (
	SELECT DISTINCT 
		osm_id as sub_osm_id, 
		name, 
		admin_level, 
		osm_id,
		level_1,
		level_2,
		level_3,
		level_4,
		level_5,
		level_6,
		level_7,
		level_8,
		level_9,
		level_10,
		level_11,
		level_12,
		level_13,
		level_14,
		level_15 FROM location
) as sub
GROUP BY osm_id, sub.name, sub.admin_level, sub.osm_id
HAVING COUNT(osm_id) > 1;

SELECT DISTINCT 
	osm_id, 
	name, 
	admin_level,
	level_1,
	level_2,
	level_3,
	level_4,
	level_5,
	level_6,
	level_7,
	level_8,
	level_9,
	level_10,
	level_11,
	level_12,
	level_13,
	level_14,
	level_15
FROM location WHERE osm_id=%s;

UPDATE public.location
	SET level_1=%s, level_2=%s, level_3=%s, level_4=%s, level_5=%s, level_6=%s, level_7=%s, level_8=%s, level_9=%s, level_10=%s, level_11=%s, level_12=%s, level_13=%s, level_14=%s, level_15=%s
	WHERE osm_id=%s AND name=%s AND admin_level=%s;