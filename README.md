# ingestion_admin_osm_data
A python script for ingesting administrative osm_data in a pgSQL database, require osm2pgsql 

## All + databse creation
Create Database : 
CREATE DATABASE yourdb;

Create extension : 
CREATE EXTENSION hstore;
CREATE EXTENSION postgis;

Then run the script:
python main.py -D=yourdb -H=<host> -P=<port> -U=<user> -W=<password> -I=<osmFilePath> -E=<osm2pgsqlPath> -oD=<nameOfOutputDatabase>


## Integration in your database
python main.py -D=yourdb -H=<host> -P=<port> -U=<user> -W=<password> -I=<osmFilePath> -E=<osm2pgsqlPath> -create=False -oD=<nameOfOutputDatabase>

## Skip osm2pgSQLPart
python main.py -D=yourdb -H=<host> -P=<port> -U=<user> -W=<password> -I=<osmFilePath> -E=<osm2pgsqlPath> -s=osm -c=False -oD=<nameOfOutputDatabase>

## Don't integrate in database
python main.py -D=yourdb -H=<host> -P=<port> -U=<user> -W=<password> -I=<osmFilePath> -E=<osm2pgsqlPath> -s=model -c=False -oD=<nameOfOutputDatabase>