import psycopg2

def loadSQLQueries(fileName, replacements=[]):
    fd = open(fileName, 'r')
    sqlFile = fd.read()
    fd.close()
    for tuple in replacements:
        sqlFile=sqlFile.replace(tuple[0], tuple[1])
    return sqlFile.split(";");

def runSQLScript(fileName, conn, replacements=[]):
    cur = conn.cursor()
    queries = loadSQLQueries(fileName, replacements)
    for query in queries:
        if (query.replace(' ', '') != ''):
            cur.execute(query)
    cur.close()

def buildInsert(rows, baseRow):
    l = [None for i in range(15)]
    levels = ["level_"+str(i+1) for i in range(15)]
    if (len(rows) != 0):

        l[baseRow[2]-1]=baseRow[0]
        for row in rows:
            if (l[row[1]-1] != None):
                raise Exception("Conflit : ", l[row[1]], " ", row[0])
            else:
                l[row[1]-1]=row[0]
    else:
        l[baseRow[2]]=baseRow[0]

    ret = l + [baseRow[0], baseRow[1], baseRow[2], baseRow[4], baseRow[3]]
    retString = "INSERT INTO public.location( "
    a = 0
    for i in l:
        a += 1
        retString += "level_" + str(a) + ", "
    retString += "osm_id, name, admin_level, way_area, way) VALUES ("
    for i in l:
        retString += '%s, '
    retString += "%s, %s, %s, %s, %s)"

    return (retString, tuple(ret))

def setupFinal(host, new_db, username, port, password, conn):
    conn2 = psycopg2.connect(host=host, database=new_db, user=username, port=port, password=password)

    cur = conn2.cursor()
    try:
        cur.execute('CREATE extension hstore;')
    except Exception as e:
        print(e)
        print('Not able to create extension hstore probably already installed : \n CREATE extensions hstore;')

    try:
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
            print(newPort, "!=", port)
        create = False

    conn = psycopg2.connect(host=host, database=database, user=username, port=port, password=password)
    conn.set_isolation_level( psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT )

    cur = conn.cursor()

    if (create):
        cur.execute("CREATE DATABASE {}".format(new_db))
    connNewDb = setupFinal(newHost, new_db, newUsername, newPort, newPassword, conn)

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
            curNew.execute(insertNamesQuery, (row[0], row[1], row[2]))

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
            query, params = buildInsert(parents, row)
            curNew.execute(query, params)

        cur.close()
        conn.commit()
        connNewDb.commit()

        runSQLScript('cleanQueries.sql', conn)

        conn.commit()

        createIndexes(connNewDb)
        connNewDb.commit()
    except Exception as e:
        runSQLScript('cleanQueries.sql', conn)
        raise e

    conn.close()
    connNewDb.close()