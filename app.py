print("ESTE ES MI APP CORRECTO")

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, jsonify
from flask_cors import CORS
from conexion import connection

app = Flask(__name__)

CORS(app, origins=["https://portelalinamarcela-bit.github.io" ])


@app.route('/')
def home():
    return jsonify({
        "mensaje": "API funcionando"
    })

#LOGIN
@app.route('/api/login', methods=['POST'])
def login():

    conexion = connection()
    cursor = conexion.cursor(dictionary=True)

    data = request.get_json()

    correo = data.get('correo')
    contrasena = data.get('contrasena')
    
    print("Correo recibido:", correo)
    print("Contraseña recibida:", contrasena)
    
    query = "SELECT * FROM usuario WHERE correoElectronico=%s"
    cursor.execute(query, (correo,))
    usuario = cursor.fetchone()

    print("Usuario encontrado:", usuario)
    
    if usuario:
        print("Hash en BD:", usuario['contrasena'])
        print("Contraseña ingresada:", contrasena)
        
        resultado = check_password_hash(usuario['contrasena'], contrasena)
        print("Resultado:", resultado)
        
        if resultado:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})

# REGISTRO
@app.route('/api/registro', methods=['POST'])
def registro():

    conexion = connection()
    cursor = conexion.cursor()

    data = request.get_json()

    nombre = data.get('nombreApellido')
    correo = data.get('correoElectronico')
    contrasena = data.get('contrasena')
    telefono = data.get('telefono')

    print("Registrando usuario:", correo)

    hash_password = generate_password_hash(contrasena)

    query = """
    INSERT INTO usuario
    (nombreApellido, correoElectronico, contrasena, telefono)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (nombre, correo, hash_password, telefono))
    conexion.commit()

    return jsonify({"success": True})

# PRODUCTOS - AGREGAR
@app.route('/api/productos', methods=['POST'])
def agregar_producto():

    conexion = connection()
    cursor = conexion.cursor()

    data = request.get_json()

    nombre = data.get('nombreProducto')
    descripcion = data.get('descripcion')
    imagen = data.get('imagen')
    porcion = data.get('porcion')
    precio = data.get('precio')
    id_categoria = data.get('id_categoria')

    query = """
    INSERT INTO productos
    (nombreProducto, descripcion, imagen, porcion, precio, id_categoria)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (nombre, descripcion, imagen, porcion, precio, id_categoria)
    )

    conexion.commit()

    return jsonify({"success": True})

# PRODUCTOS - LISTAR
@app.route('/api/productos', methods=['GET'])
def obtener_productos():

    conexion = connection()
    cursor = conexion.cursor(dictionary=True)

    query = """
    SELECT p.*, c.nombre
    FROM productos p
    INNER JOIN categoria c
    ON p.id_categoria = c.id_categoria
    """

    cursor.execute(query)

    productos = cursor.fetchall()

    return jsonify(productos)

# PEDIDOS - REGISTRAR
@app.route('/api/pedidos', methods=['POST'])
def crear_pedido():

    conexion = connection()
    cursor = conexion.cursor()

    data = request.get_json()

    id_usuario = data.get('id_usuario')
    total = data.get('total')
    ubicacion = data.get('ubicacion')
    metodo_pago = data.get('metodo_pago')

    query = """
    INSERT INTO pedido
    (id_usuario, fecha, estado, total, ubicacion, metodo_pago)
    VALUES (%s, NOW(), %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            id_usuario,
            "Pendiente",
            total,
            ubicacion,
            metodo_pago
        )
    )

    conexion.commit()

    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(port=3000, debug=True)