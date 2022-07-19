# Connect to db
from mysql.connector import connect

dbapi = connect(
    host = 'localhost',
    user = 'root',
    database = 'laravel',
    port = 8888
)

cursor = dbapi.cursor()
cursor.execute('SELECT * FROM users LIMIT 100;')