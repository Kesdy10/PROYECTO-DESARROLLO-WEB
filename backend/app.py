from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://usuario:password@localhost:5432/dongato')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellidos = db.Column(db.String(100), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)

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
    app.run(debug=True)
