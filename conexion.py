import mysql.connector


def connection():
    host = 'arcela.proxy.rlwy.net'
    port = 15183
    user = 'root'
    password = 'LqExHhecKrEUiqqDnJSYoeuhGfIRqFUI'
    database = 'railway'

    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        print("Conexión exitosa a la base de datos")
        return conn

    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None