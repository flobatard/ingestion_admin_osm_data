import psycopg2
import solidifyParentsParents as cleanParents

def loadSQLQueries(fileName, replacements=[]):
    fd = open(fileName, 'r')
    sqlFile = fd.read()
    fd.close()
    for tuple in replacements:
        sqlFile=sqlFile.replace(tuple[0], tuple[1])
    return sqlFile.split(";")

def runSQLScript(fileName, conn, replacements=[]):
    cur = conn.cursor()
    queries = loadSQLQueries(fileName, replacements)
    for query in queries:
        if (query.replace(' ', '') != ''):
            print(query)
            cur.execute(query)
    cur.close()
    
def buildSameLocationQuery():
    findQuery = "SELECT id, osm_id, level_1, level_2, level_3, level_4, level_5, \
        level_6, level_7, level_8, level_9, level_10, \
        level_11, level_12, level_13, level_14, level_15,\
        way, way_area \
        FROM public.location \
        WHERE osm_id=%(osm_id)s AND \
        ( (ST_AREA(ST_INTERSECTION(%(way)s, way)))/way_area > 0.95 OR (ST_AREA(ST_INTERSECTION(%(way)s, way)))/%(way_area)s > 0.95 ) \
        "
    return findQuery

def deleteIds(ids, cur):
    query = "DELETE FROM public.location WHERE id=ANY(%(ids)s)"
    cur.execute(query, {"ids": ids})
    
#insert_to_do_:    
#{
#   osm_id: osm_id
#   name: name
#   admin_level: admin_level
#   way: way
#   way_area: way_area
#   level_1: 
#   level_2:
#   ...
#   level_15:
#}
#    
def buildInsertString(insert_to_do):
    retString = "INSERT INTO public.location( "
    retString += ", ".join(map(lambda x: str(x), insert_to_do.keys())) + ")\n VALUES ("
    retString += ", ".join(map(lambda x: "%({})s".format(str(x)), insert_to_do.keys())) + ")\n ON CONFLICT (level_1, level_2, level_3, level_4, \
                                level_5, level_6, level_7, level_8,\
                                level_9, level_10, level_11, level_12,\
                                level_13, level_14, level_15,\
                                osm_id, way_area) DO UPDATE SET "
    equals = []
    for key in insert_to_do.keys():
        equals.append("{0}=%({0})s".format(key))
    retString += ", ".join(equals) + "\n WHERE location.osm_id=%(osm_id)s AND location.way_area=%(way_area)s"
    return retString

def buildUpdateString(insert_to_do, id):
    retString = "UPDATE public.location SET "
    equals = []
    for key in insert_to_do.keys():
        if (key != "id"):
            equals.append("{0}=%({0})s".format(key))
    retString += ", ".join(equals) + "\n WHERE location.id=%(id)s"
    insert_to_do["id"] = id
    return retString

#[["a", "b"],["c"],[]] -> [["a","c",None], ["b","c",None]]
#[["a", "b"], ["1, 3"], [], ["A"], []] -> [["a", "1", None, "A", None], ["b", "1", None, "A", None], ["a", "3", None, "A", None], ["b", "3", None, "A", None]]
#
def combineList(l):
    if (l==[]):
        return []
    l2 = l[0]
    if (len(l) == 1):
        if (len(l2) == 0):
            return [[None]]
        else:
            return list(map(lambda x: [x], l2))

    if (len(l2) == 0):
        return list(map(lambda x: [None] + x, combineList(l[1:])))
    elif (len(l2) == 1):
        return list(map(lambda x: [l2[0]] + x, combineList(l[1:])))
    else:
        ret = []
        for li in combineList(l[1:]):
            for possibility in l2:
                ret.append([possibility] + li)
        return ret

#Base Row [osm_id, name, admin_level, way, way_area]
def buildInsertsData(parents, baseRow):
    osm_id = baseRow[0]
    name = baseRow[1]
    admin_level = baseRow[2]
    way = baseRow[3]
    way_area = baseRow[4]
    l = [[] for i in range(15)]
    levels = ["level_"+str(i+1) for i in range(len(l))]
    l[admin_level-1]=[osm_id]
    #Parent [osm_id, admin_level, name, admin_level_of_baseRow(useless)]
    for parent in parents:
        parent_osm_id = parent[0]
        parent_admin_level = parent[1]
        l[parent_admin_level - 1].append(parent_osm_id)
    
    final_list = combineList(l)
    ret = []
    if (len(final_list) > 1):
        print("MULTIPLE PARENTS: ", final_list)
    for parents_osm in final_list:
        insert_to_do = {
            "osm_id" : osm_id,
            "name" : name,
            "admin_level" : admin_level,
            "way" : way,
            "way_area" : way_area
        }
        for i in range(len(levels)):
            insert_to_do[levels[i]] = parents_osm[i]
        ret.append(insert_to_do)
    return ret

#Base Row [osm_id, name, admin_level, way, way_area]
def buildInserts(parents, baseRow):    
    inserts_to_do = buildInsertsData(parents, baseRow)
    
    retStrings = list(map(lambda x: buildInsertString(x), inserts_to_do))

    return (retStrings, inserts_to_do)

def setupFinal(host, new_db, username, port, password):
    print("CONNECTING TO FINAL DB: host={0} db_name={1} username={2} port={3} password={4}".format(host, new_db, username, port, password))
    conn2 = psycopg2.connect(host=host, database=new_db, user=username, port=port, password=password)
    print("CONNECTED")
    cur = conn2.cursor()
    try:
        print('CREATE extension hstore;')
        cur.execute('CREATE extension hstore;')
    except Exception as e:
        print(e)
        print('Not able to create extension hstore probably already installed : \n CREATE extensions hstore;')

    try:
        print('CREATE extension postgis;')
        cur.execute('CREATE extension postgis;')
    except Exception as e:
        print(e)
        print('Not able to create extension postgis probably already installed : \n CREATE extensions postgis;')
    conn2.commit()
    conn2.close()
    conn2 = psycopg2.connect(host=host, database=new_db, user=username, port=port, password=password)

    runSQLScript('setupFinalQueries.sql', conn2)

    return conn2

def createIndexes(conn):
    cur = conn.cursor()

    queries = loadSQLQueries('setupIndexes.sql');
    index_level = queries[4]
    runSQLScript('setupIndexes.sql', conn, [('$1', '1')])

    for i in range(2,16):
        cur.execute(index_level.replace('$1', str(i)))
    cur.close()

def enrichDataWithSameLocation(data_to_insert, same_location_data):
    ret = []
    changes = False
    for i in range(len(data_to_insert)):
        to_insert = {
            "id": same_location_data[i]["id"],
            "osm_id": data_to_insert[i]["osm_id"],
            "level_1": data_to_insert[i]["level_1"] or same_location_data[i]["level_1"],
            "level_2": data_to_insert[i]["level_2"] or same_location_data[i]["level_2"],
            "level_3": data_to_insert[i]["level_3"] or same_location_data[i]["level_3"],
            "level_4": data_to_insert[i]["level_4"] or same_location_data[i]["level_4"],
            "level_5": data_to_insert[i]["level_5"] or same_location_data[i]["level_5"],
            "level_6": data_to_insert[i]["level_6"] or same_location_data[i]["level_6"],
            "level_7": data_to_insert[i]["level_7"] or same_location_data[i]["level_7"],
            "level_8": data_to_insert[i]["level_8"] or same_location_data[i]["level_8"],
            "level_9": data_to_insert[i]["level_9"] or same_location_data[i]["level_9"],
            "level_10": data_to_insert[i]["level_10"] or same_location_data[i]["level_10"],
            "level_11": data_to_insert[i]["level_11"] or same_location_data[i]["level_11"],
            "level_12": data_to_insert[i]["level_12"] or same_location_data[i]["level_12"],
            "level_13": data_to_insert[i]["level_13"] or same_location_data[i]["level_13"],
            "level_14": data_to_insert[i]["level_14"] or same_location_data[i]["level_14"],
            "level_15": data_to_insert[i]["level_15"] or same_location_data[i]["level_15"],
            "way": data_to_insert[i]["way"],
            "way_area": data_to_insert[i]["way_area"]
        }
        if (to_insert != same_location_data[i]):
            changes = True
        ret.append(to_insert)
    return (changes and ret)


def baseModelToContainsModel(host ,database ,username, password, port=5432, new_db='osm_data', newHost=None, newUsername=None, newPassword=None, newPort=None, create=True):

    if (newHost == None):
        newHost = host

    if (newUsername == None):
        newUsername = username

    if (newPassword == None):
        newPassword = password

    if (newPort == None):
        newPort = port

    if (newHost != host or username != newUsername or newPassword != password or newPort != port):
        print("Update mode forced because connection data changed: ")
        if (newHost != host):
            print(newHost, "!=", host)
        if (newUsername != username):
            print(newUsername, "!=", username)
        if (newPassword != password):
            print(newPassword, "!=", password)
        if (newPort != port):
            print(int(newPort), "!=", int(port))
        create = False


    print("CONNECTING TO OSM_DB : host=", host, " db_name=", database, " username=", username, " port=", port, " password=", password)
    conn = psycopg2.connect(host=host, database=database, user=username, port=int(port), password=password)
    print("CONNECTED")
    conn.set_isolation_level( psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT )

    cur = conn.cursor()
    if (create):
        print("SELECT 1 FROM pg_database WHERE datname = '{0}'".format(new_db))
        cur.execute("SELECT 1 FROM pg_database WHERE datname = '{0}'".format(new_db))
        res = cur.fetchall()
        print(res)
        if (len(res) == 0):
            print("CREATE DATABASE \"{}\"".format(new_db))
            cur.execute("CREATE DATABASE \"{}\"".format(new_db))
            
    connNewDb = setupFinal(newHost, new_db, newUsername, newPort, newPassword)

    runSQLScript('setupQueries.sql', conn, [('$1', new_db)])
    try:

        queries = loadSQLQueries('mainQueries.sql')
        queryAll = queries[0]
        queryUpperAdminLevel = queries[2]

        queries = loadSQLQueries('namesQueries.sql')
        selectNamesQuery = queries[0]
        insertNamesQuery = queries[1]

        curNewNames = connNewDb.cursor()
        
        curNewDelIns = connNewDb.cursor()

        cur.execute(selectNamesQuery)
        rows = cur.fetchall()

        for row in rows:
            curNewNames.execute(insertNamesQuery, {"osm_id" : row[0], "name" : row[1], "admin_level" : row[2]})
            
        curNewSameLocation = connNewDb.cursor()

        cur.execute(queryAll)

        sameLocationQuery = buildSameLocationQuery()

        rows = cur.fetchall()
        i = 0
        
        full_inserted = 0
        deleted_by_replaced = 0
        inserted_by_replace = 0
        updated_with_multiple_parents = 0
        updated_by_replace = 0
        not_touched = 0
        #row [osm_id, name, admin_level, way, way_area]
        for row in rows:
            i += 1
            if (i%100 == 0):
                print(i, "/", len(rows), " : ", row[1])
            osm_id = row[0]
            way = row[3]
            way_area = row[4]
            cur.execute(queryUpperAdminLevel, (osm_id, way))
            parents = cur.fetchall()
            
            curNewSameLocation.execute(sameLocationQuery, {"osm_id": osm_id, "way": way, "way_area": way_area})
            sameLocations = curNewSameLocation.fetchall()
            
            querys, params = buildInserts(parents, row)
            
            inserts_to_do = buildInsertsData(parents, row)
            
            sameLocations = list(map(lambda x : 
                {
                    "id": x[0],
                    "osm_id": x[1],
                    "level_1": x[2],
                    "level_2": x[3],
                    "level_3": x[4],
                    "level_4": x[5],
                    "level_5": x[6],
                    "level_6": x[7],
                    "level_7": x[8],
                    "level_8": x[9],
                    "level_9": x[10],
                    "level_10": x[11],
                    "level_11": x[12],
                    "level_12": x[13],
                    "level_13": x[14],
                    "level_14": x[15],
                    "level_15": x[16],
                    "way": x[17],
                    "way_area": x[18]
                }, sameLocations))
        
            
            if (len(sameLocations) == 0):
                #WAS NOT IN
                querys = list(map(lambda x: buildInsertString(x), inserts_to_do))
                for j in range(len(querys)):
                    full_inserted += 1
                    curNewDelIns.execute(querys[j], inserts_to_do[j])
            elif (len(sameLocations) != len(inserts_to_do)):
                #DELETE
                ids = list(map(lambda x: x["id"], sameLocations))
                deleteIds(ids, curNewDelIns)
                deleted_by_replaced += len(ids)
                querys = list(map(lambda x: buildInsertString(x), inserts_to_do))
                for j in range(len(querys)):
                    inserted_by_replace += 1
                    curNewDelIns.execute(querys[j], inserts_to_do[j])
            else:
                #UPDATES
                ids = list(map(lambda x: x["id"], sameLocations))
                enriched_inserts = enrichDataWithSameLocation(inserts_to_do, sameLocations)
                if (enriched_inserts):
                    querys = list(map(lambda enriched_ins: buildUpdateString(enriched_ins, enriched_ins["id"]), enriched_inserts))
                    params = enriched_inserts
                    
                    for j in range(len(querys)):
                        if (len(querys) > 1):
                            updated_with_multiple_parents += 1
                        else:
                            updated_by_replace += 1
                        curNewDelIns.execute(querys[j], params[j])
                else:
                    not_touched += len(ids)

        cur.close()
        curNewDelIns.close()
        conn.commit()
        connNewDb.commit()
        runSQLScript('cleanQueries.sql', conn)

        conn.commit()
        runSQLScript('searchTableQueries.sql', connNewDb)
        createIndexes(connNewDb)
        connNewDb.commit()
        
        print("FULL INSERT: ", full_inserted)
        print("DELETED BY REPLACED: ", deleted_by_replaced)
        print("INSERTED BY REPLACE: ",inserted_by_replace)
        print("UPDATED BY REPLACE: ", updated_by_replace)
        print("UPDATED PARENTS: ", updated_with_multiple_parents)
        print("NOT TOUCHED: ", not_touched)
        
    except Exception as e:
        runSQLScript('cleanQueries.sql', conn)
        raise e

    conn.close()
    connNewDb.close()