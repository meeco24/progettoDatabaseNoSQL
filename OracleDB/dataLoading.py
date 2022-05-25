import cx_Oracle

#connessione al db

#formato connectionString: <username>/<password>@<dbHostAddress>:<dbPort>/<dbServiceName>
conStr = 'system/ciccio@localhost:1521/ORCLPDB1'

conn = cx_Oracle.connect(conStr)

print(conn)

cursor = conn.cursor()

#queries

cursor.close()