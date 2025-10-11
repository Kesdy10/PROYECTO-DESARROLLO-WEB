from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from flask import send_from_directory
from flask import render_template
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Conexión a Railway PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:FvYWODdjiusyFFvUOBIOnDWTjbAOXQEV@centerbeam.proxy.rlwy.net:36876/railway'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
print("Conectado a la base de datos:", db.engine.url)

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellidos = db.Column(db.String(100), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)

# === RUTAS DE PÁGINAS ===
@app.route('/')
def home():
    return render_template('ventanas/login.html')

@app.route('/login.html')
def login_page():
    return render_template('ventanas/login.html')

@app.route('/crearCuenta.html')
def crear_cuenta_page():
    return render_template('ventanas/crearCuenta.html')

@app.route('/index.html')
def index():
    return render_template('ventanas/index.html')

@app.route('/cuenta.html')
def cuenta():
    return render_template('ventanas/cuenta.html')

@app.route('/contacto.html')
def contacto():
    return render_template('ventanas/contacto.html')

@app.route('/carrito.html')
def carrito():
    return render_template('ventanas/carrito.html')

# === CATÁLOGOS DE MARCAS ===
@app.route('/nike.html')
def nike():
    return render_template('ventanas/nike.html')

@app.route('/adidas.html')
def adidas():
    return render_template('ventanas/adidas.html')

@app.route('/newbalance.html')
def newbalance():
    return render_template('ventanas/newbalance.html')

@app.route('/puma.html')
def puma():
    return render_template('ventanas/puma.html')

@app.route('/converse.html')
def converse():
    return render_template('ventanas/converse.html')

@app.route('/vans.html')
def vans():
    return render_template('ventanas/vans.html')

# === PRODUCTOS ===
@app.route('/nikegato.html')
def nikegato():
    return render_template('productosNike/nikegato.html')

# === API ENDPOINTS ===

# Endpoint para crear usuario
@app.route('/api/usuario', methods=['POST'])
def crear_usuario():
    data = request.json
    usuario = Usuario(
        apellidos=data.get('apellidos'),
        nombres=data.get('nombres'),
        correo=data.get('correo'),
        telefono=data.get('telefono'),
        fecha_nacimiento=data.get('fecha_nacimiento'),
        genero=data.get('genero'),
        direccion=data.get('direccion')
    )
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado', 'id': usuario.id})

# Endpoint para obtener todos los usuarios
@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    resultado = []
    for u in usuarios:
        resultado.append({
            'id': u.id,
            'apellidos': u.apellidos,
            'nombres': u.nombres,
            'correo': u.correo,
            'telefono': u.telefono,
            'fecha_nacimiento': str(u.fecha_nacimiento),
            'genero': u.genero,
            'direccion': u.direccion
        })
    return jsonify(resultado)

# Endpoint para actualizar usuario
@app.route('/api/usuario/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json
    usuario.apellidos = data.get('apellidos', usuario.apellidos)
    usuario.nombres = data.get('nombres', usuario.nombres)
    usuario.correo = data.get('correo', usuario.correo)
    usuario.telefono = data.get('telefono', usuario.telefono)
    usuario.fecha_nacimiento = data.get('fecha_nacimiento', usuario.fecha_nacimiento)
    usuario.genero = data.get('genero', usuario.genero)
    usuario.direccion = data.get('direccion', usuario.direccion)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario actualizado'})

# Endpoint para borrar usuario
@app.route('/api/usuario/<int:id>', methods=['DELETE'])
def borrar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario borrado'})

@app.route('/api/crear-cuenta', methods=['POST'])
def crear_cuenta():
    data = request.get_json()
    try:
        usuario = Usuario(
            apellidos=data['apellidos'],
            nombres=data['nombres'],
            correo=data['correo'],
            telefono=data['telefono'],
            fecha_nacimiento=data['fecha_nacimiento'],
            genero=data['genero'],
            direccion=data['direccion']
        )
        db.session.add(usuario)
        db.session.commit()
        return jsonify({'mensaje': 'Cuenta creada exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)