#The goal here is in the db location their can be the same osm_id for multiple line due to non connex
#locations (example Bretagne with island or Lorient or Grass)

#Some of those can unfortunaly end up in locations that are not conatained in the parant, we end up with
#Multiple locations that have tha same osm_id but not the same level_i columns
#We are here to correct that

def loadSQLQueries(fileName, replacements=[]):
    fd = open(fileName, 'r')
    sqlFile = fd.read()
    fd.close()
    for tuple in replacements:
        sqlFile=sqlFile.replace(tuple[0], tuple[1])
    return sqlFile.split(";")

def cleanDataOutOfParents(conn):
    cur = conn.cursor()
    
    
    queries = loadSQLQueries('cleanDataOutOfParents.sql')
    get_bad_osm_ids = queries[0]
    
    get_levels_from_osm_id = queries[1]
    
    update_query = queries[2]
    
    cur.execute(get_bad_osm_ids)
    rows = cur.fetchAll()
    
    #[count, name, admin_level, osm_id]
    for bad_osm_line in rows:
        name = bad_osm_line[1]
        admin_level = bad_osm_line[2]
        osm_id = bad_osm_line[3]
        cur.execute(get_levels_from_osm_id, (osm_id,))
        
        #[[osm_id, name, admin_level, level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8, level_9,
	    #level_10, level_11, level_12, level_13, level_14, level_15]]
        to_merge = cur.fetchAll() #Here we have all the different level we want to kind of "merge"
        merge_levels(osm_id, name, admin_level, to_merge, cur)
        
    cur.close()
    conn.commit()

def merge_levels(osm_id, name, admin_level, to_merge, cur):
    levels = [None for i in range(15)]
    #[osm_id, name, admin_level, level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8, level_9,
	#level_10, level_11, level_12, level_13, level_14, level_15]
    for i in range(len(levels)):
        levels[i] = get_all_from_column(to_merge, i+3) #+3 for offset because level_1

    for i in range(len(levels)):
        try:
            levels[i] = get_the_remaining_from_osm(levels[i])
        except Exception as e:
            print(e)
            print("Same parent for level_{} for osm_id {} : {} (admin_level: {})".format(i+1, osm_id, name, admin_level))
    
    for line in to_merge:
        cur.execute(update_query, levels + [osm_id, name, admin_level])
        
    
    
    

def get_all_from_column(matrix, column):
    return [i[column] for i in matrix]

def get_the_remaining_from_osm(l):
    to_keep = None
    for i in l:
        if i != None:
            if to_keep != None and to_keep != i:
                raise Exception({"message": "Different parent for same admin id", "value": l})
            to_keep = i
    return to_keep
            