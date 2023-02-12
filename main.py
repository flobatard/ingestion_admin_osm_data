import psycopg2
import os
import getopt
import argparse
import sys
import time
## The model to pass from osm data_strucutre to tree strucure containing all contained polygones
import baseModelToContainsModel as BM2CM

def execute_osm2pgsql(host, db, user, password, osm2pgsqlPath, stylePath, osmDataPath):
    cmd = '{} -c -d {} -U {} -W -S {} -H {} {}'.format(osm2pgsqlPath, db, user, stylePath, host, osmDataPath)
    print(cmd)
    os.system(cmd)
    print('ENDED')

def createArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--database', help='name of the database')
    parser.add_argument('-H', '--host', help='the host of the database', default='localhost')
    parser.add_argument('-P', '--port', type=int, help='port of the database', default=5432)
    parser.add_argument('-U', '--username', help='username of the database', default='postgres')
    parser.add_argument('-S', '--style', help='.style path', default='custom.style')
    parser.add_argument('-E', '--exeosm2pgsql', help='Path to osm2pgsql exe file', default='osm2pgsql')
    parser.add_argument('-W', '--password', help='Password of the database (you will need to retype it on the following prompt)')
    parser.add_argument('-I', '--inputFile', help='Path to osm data file')
    parser.add_argument('-oD', '--outputDatabase', help='name of the database where the output data are put (can be the same as -D option)', default='osm_data')
    parser.add_argument('-c', '--create', help='If true then create the output database else the output database is supposed already created (default value=true)', default='true', required=False)

    parser.add_argument('-oH', '--outputHost', help='the host of the output database (note if this argument is provided then -c is automatically put to false)', required=False)

    parser.add_argument('-oP', '--outputPort', help='the port of the output database (note if this argument is provided then -c is automatically put to false)', required=False)

    parser.add_argument('-oU', '--outputUser', help='the username of the output database (note if this argument is provided then -c is automatically put to false)', required=False)

    parser.add_argument('-oW', '--outputPassword', help='the password of the output database (note if this argument is provided then -c is automatically put to false)', required=False)

    parser.add_argument('-s', '--skip', help='can be either osm or model, osm to skip the osm2pgsql part and model to skip the model transition part', default=None)
    return parser


if (__name__ == '__main__'):
    initPath = os.getcwd()
    togo = (os.sep).join(sys.argv[0].split(os.sep)[:-1])

    argParser = createArgs()
    args = argParser.parse_args()

    if (args.skip != 'osm'):
        execute_osm2pgsql(args.host, args.database, args.username, args.password, args.exeosm2pgsql, args.style, args.inputFile)
    create = False



    if (args.create == 'true' and args.outputHost==None and args.outputPassword==None and args.outputPort==None and args.outputUser==None):
        create = True
    if (togo != ''):
        os.chdir(togo)

    if (args.skip != 'model'):
        BM2CM.baseModelToContainsModel(args.host, args.database, args.username, args.password, args.port, args.outputDatabase, args.outputHost, args.outputUser, args.outputPassword, args.outputPort, create)

    os.chdir(initPath)

    print('DONE')
