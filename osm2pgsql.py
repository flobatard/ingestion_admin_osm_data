import psycopg2
import os

def setup_extensions(host, db, user, password, port):

    try:
        conn = psycopg2.connect(host=host, database=db, user=user, port=port, password=password)
    except Exception as e:
        print("HOST: ", host)
        print("DB: ", db)
        print("USER: ", user)
        print("PORT: ", port)
        print("NOT ABLE TO CONNECT TO THIS DB")
        raise e
        
    print("CONNECTED")
    cur = conn.cursor()
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
    conn.commit()
    conn.close()
    
def execute_osm2pgsql(host, db, user, password, osm2pgsqlPath, stylePath, osmDataPath):
    cmd = '{} -c -d {} -U {} -W -S {} -H {} {}'.format(osm2pgsqlPath, db, user, stylePath, host, osmDataPath)
    print(cmd)
    os.system(cmd)
    print('ENDED')
    
def integrate_osm_data(host, db, user, password, port, osm2pgsqlPath, stylePath, osmDataPath):
    setup_extensions(host, db, user, password, port)
    execute_osm2pgsql(host, db, user, password, osm2pgsqlPath, stylePath, osmDataPath)
    