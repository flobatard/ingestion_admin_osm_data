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
        queryUpperAdminLevel = queries[1]

        queries = loadSQLQueries('namesQueries.sql')
        selectNamesQuery = queries[0]
        insertNamesQuery = queries[1]


        curNew = connNewDb.cursor()

        cur.execute(selectNamesQuery)
        rows = cur.fetchall()

        for row in rows:
            curNew.execute(insertNamesQuery, {"osm_id" : row[0], "name" : row[1], "admin_level" : row[2]})

        cur.execute(queryAll)

        rows = cur.fetchall()
        i = 0
        for row in rows:
            i += 1
            print(i, "/", len(rows), " : ", row[1])
            osm_id = row[0]
            way = row[3]
            cur.execute(queryUpperAdminLevel, (osm_id, way))

            parents = cur.fetchall()
            querys, params = buildInserts(parents, row)
            for j in range(len(querys)):
                curNew.execute(querys[j], params[j])

        cur.close()
        conn.commit()
        connNewDb.commit()
        runSQLScript('cleanQueries.sql', conn)

        conn.commit()
        runSQLScript('searchTableQueries.sql', connNewDb)
        createIndexes(connNewDb)
        connNewDb.commit()
    except Exception as e:
        runSQLScript('cleanQueries.sql', conn)
        raise e

    conn.close()
    connNewDb.close()