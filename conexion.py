import mysql.connector
impor os

def connection():

    try:
        conn= mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),
            port=os.getenv("MYSQLPORT"),
            user=os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE")
        )

        print("Conexión exitosa a la base de datos")
        return conn
    
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None
    
    