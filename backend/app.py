from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
import os

app = Flask(__name__)

# Conexión a Railway PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:FvYWODdjiusyFFvUOBIOnDWTjbAOXQEV@postgres.railway.internal:5432/railway'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellidos = db.Column(db.String(100))
    nombres = db.Column(db.String(100))
    correo = db.Column(db.String(120), unique=True)
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.String(1))  # 'M' o 'F'
    direccion = db.Column(db.String(255))

# Inicializa la base de datos (solo la primera vez)
# Ejecuta esto en la terminal de Python:
# >>> from app import db
# >>> db.create_all()

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