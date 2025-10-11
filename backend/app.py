from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://usuario:password@localhost:5432/dongato')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
def login():
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