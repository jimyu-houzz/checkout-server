import mysql.connector

# TODO: use .env file
connection_conf_d = {
    'host': "localhost",
    'user': "root",
    'password': "root",
    'database': 'test_db',
    'port': 3307
}

conn = mysql.connector.connect(**connection_conf_d)
