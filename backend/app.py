from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import inspect
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuración de la base de datos
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_muy_segura_para_railway_2024')  

# Configurar base de datos PostgreSQL para Railway
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Arreglar el protocolo si es necesario (Railway a veces usa postgres:// en lugar de postgresql://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"✅ Conectando a PostgreSQL: {database_url[:30]}...")
else:
    # Fallback local a SQLite para evitar errores cuando no hay PostgreSQL local
    print("❌ No se encontró DATABASE_URL — usando SQLite local (dongato.db)")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dongato.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_timeout': 20,
    'pool_recycle': 300,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    nacimiento = db.Column(db.Date, nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Mensaje
class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Mensaje {self.nombre}>'

# Modelo de Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    tallas_disponibles = db.Column(db.String(200), nullable=False)  # "6,7,8,9,10,11,12"
    imagen_ruta = db.Column(db.String(300), nullable=True)
    pagina_html = db.Column(db.String(100), nullable=True)  # nikegato.html
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'
    
    def get_tallas(self):
        """Retorna lista de tallas disponibles como strings (soporta medias tallas)."""
        return [t.strip() for t in self.tallas_disponibles.split(',') if t.strip()]

def seed_or_update_products():
    """Crea o actualiza productos base con precios únicos dentro de los rangos dados.
    Es idempotente: si el producto (por pagina_html) existe, actualiza; si no, inserta.
    """
    tallas_default = '5.5,6,6.5,7,7.5,8,8.5,9,9.5,10'

    productos_def = [
        # NIKE (existentes)
        dict(nombre='Nike Gato SB', marca='Nike', precio=1000, pagina_html='nikegato.html'),
        dict(nombre='Nike Air Jordan 1 Mid', marca='Nike', precio=1400, pagina_html='nikeairjordan1mid.html'),
        dict(nombre='Nike Air Max Nuaxis', marca='Nike', precio=1200, pagina_html='nikeairmaxnuaxis.html'),
        dict(nombre='Nike P-6000', marca='Nike', precio=1100, pagina_html='nikep6000.html'),
        dict(nombre='Nike Pegasus Plus', marca='Nike', precio=1300, pagina_html='nikepegasusplus.html'),
        dict(nombre='Nike Premier III', marca='Nike', precio=950, pagina_html='nikepremieriii.html'),

        # NEW BALANCE
        dict(nombre='New Balance 574', marca='New Balance', precio=800, pagina_html='newbalance574.html'),
        dict(nombre='New Balance 740', marca='New Balance', precio=700, pagina_html='newbalance740.html'),
        dict(nombre='New Balance 990v6', marca='New Balance', precio=1900, pagina_html='newbalance990v6.html'),
        dict(nombre='New Balance 997R', marca='New Balance', precio=1000, pagina_html='newbalance997r.html'),
        dict(nombre='New Balance 2002R', marca='New Balance', precio=1300, pagina_html='newbalance2002r.html'),
        dict(nombre='New Balance 9060', marca='New Balance', precio=1500, pagina_html='newbalance9060.html'),

        # ADIDAS
        dict(nombre='Adidas Adizero', marca='Adidas', precio=1300, pagina_html='adidasadizero.html'),
        dict(nombre='Adidas Campus', marca='Adidas', precio=800, pagina_html='adidascampus.html'),
        dict(nombre='Adidas Gazelle', marca='Adidas', precio=900, pagina_html='adidasgazelle.html'),
        dict(nombre='Adidas Kaptir', marca='Adidas', precio=700, pagina_html='adidaskaptir.html'),
        dict(nombre='Adidas Samba', marca='Adidas', precio=1100, pagina_html='adidassamba.html'),
        dict(nombre='Adidas Ultraboost', marca='Adidas', precio=1800, pagina_html='adidasultraboost.html'),

        # CONVERSE
        dict(nombre='Converse Chuck 70', marca='Converse', precio=650, pagina_html='conversechuck70.html'),
        dict(nombre='Converse Chuck Taylor', marca='Converse', precio=500, pagina_html='conversechucktaylor.html'),
        dict(nombre='Converse CL98', marca='Converse', precio=650, pagina_html='conversecl98.html'),
        dict(nombre='Converse Fastbreak', marca='Converse', precio=900, pagina_html='conversefastbreak.html'),
        dict(nombre='Converse Run Star', marca='Converse', precio=1200, pagina_html='converserunstar.html'),
        dict(nombre='Converse Wave', marca='Converse', precio=900, pagina_html='conversewave.html'),

        # VANS
        dict(nombre='Vans Chukka', marca='Vans', precio=700, pagina_html='vanschukka.html'),
        dict(nombre='Vans Classic Slip', marca='Vans', precio=600, pagina_html='vansclassicslip.html'),
        dict(nombre='Vans Old Skool', marca='Vans', precio=550, pagina_html='vansoldskool.html'),
        dict(nombre='Vans Sk8-Hi', marca='Vans', precio=750, pagina_html='vanssk8hi.html'),
        dict(nombre='Vans Super Low Pro', marca='Vans', precio=800, pagina_html='vanssuperlowpro.html'),
        dict(nombre='Vans UltraRange', marca='Vans', precio=900, pagina_html='vansultrarange.html'),

        # REEBOK
        dict(nombre='Reebok Classic Nylon', marca='Reebok', precio=650, pagina_html='reebokclassicnylon.html'),
        dict(nombre='Reebok Fiori', marca='Reebok', precio=550, pagina_html='reebokfiori.html'),
        dict(nombre='Reebok Floatzig', marca='Reebok', precio=1000, pagina_html='reebokfloatzig.html'),
        dict(nombre='Reebok Nano', marca='Reebok', precio=1300, pagina_html='reeBoknano.html'),
        dict(nombre='Reebok Phase Court', marca='Reebok', precio=700, pagina_html='reebokphasecourt.html'),
        dict(nombre='Reebok Question', marca='Reebok', precio=1500, pagina_html='reebokquestion.html'),
    ]

    inserted, updated = 0, 0
    for p in productos_def:
        existente = Producto.query.filter_by(pagina_html=p['pagina_html']).first()
        if existente:
            # Actualizar precio y campos básicos si cambiaron
            cambios = 0
            if existente.precio != p['precio']:
                existente.precio = p['precio']
                cambios += 1
            if existente.nombre != p['nombre']:
                existente.nombre = p['nombre']
                cambios += 1
            if existente.marca != p['marca']:
                existente.marca = p['marca']
                cambios += 1
            if existente.tallas_disponibles != tallas_default:
                existente.tallas_disponibles = tallas_default
                cambios += 1
            if cambios:
                updated += 1
        else:
            nuevo = Producto(
                nombre=p['nombre'],
                marca=p['marca'],
                precio=p['precio'],
                tallas_disponibles=tallas_default,
                imagen_ruta=None,
                pagina_html=p['pagina_html']
            )
            db.session.add(nuevo)
            inserted += 1

    if inserted or updated:
        db.session.commit()
    print(f"✅ Productos: insertados={inserted}, actualizados={updated}, total={Producto.query.count()}")

# Inicializar la base de datos
try:
    with app.app_context():
        db.create_all()
        seed_or_update_products()
except Exception as e:
    print(f"Error al inicializar BD: {e}")

# VENTANAS
@app.route('/health')
def health_check():
    """Endpoint de verificación de salud para Railway"""
    try:
        # Verificar conexión a la base de datos
        with app.app_context():
            result = db.session.execute('SELECT 1').scalar()
            
        # Verificar que las tablas existen
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        return {
            'status': 'healthy', 
            'database': 'connected',
            'tables': len(tables),
            'tables_list': tables
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy', 
            'database': 'disconnected',
            'error': str(e)
        }, 500

# Manejo global de errores
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('ventanas/login.html'), 500


@app.route('/')
def login():
    return render_template('ventanas/login.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validaciones básicas
        if not email or not password:
            return render_template('ventanas/login.html')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nombres + ' ' + (usuario.apellidos or '')
            return redirect(url_for('index'))
        # Credenciales inválidas: volver a mostrar login (sin mensajes flash)
        return render_template('ventanas/login.html')
    
    return render_template('ventanas/login.html')

@app.route('/crearCuenta.html', methods=['GET', 'POST'])
def crear_cuenta():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos', '')
        email = request.form.get('email')
        telefono = request.form.get('telefono', '')
        nacimiento = request.form.get('nacimiento')
        direccion = request.form.get('direccion', '')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones básicas
        if not nombres or not email or not password:
            return render_template('ventanas/crearCuenta.html')
            
        # Validar confirmación de contraseña
        if password != confirm_password:
            return render_template('ventanas/crearCuenta.html')
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(email=email).first():
            return render_template('ventanas/crearCuenta.html')
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            telefono=telefono,
            direccion=direccion
        )
        
        # Manejar fecha de nacimiento
        if nacimiento:
            nuevo_usuario.nacimiento = datetime.strptime(nacimiento, '%Y-%m-%d').date()
        
        nuevo_usuario.set_password(password)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return render_template('ventanas/crearCuenta.html')
    
    return render_template('ventanas/crearCuenta.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/index.html')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('ventanas/index.html')

@app.route('/cuenta.html', methods=['GET', 'POST'])
def cuenta():
    # Si no hay usuario logueado, redirigir a login solo para cuenta
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Obtener datos del formulario (normalizados)
        nombres = (request.form.get('nombres') or '').strip()
        apellidos = (request.form.get('apellidos') or '').strip()
        email = (request.form.get('email') or '').strip()
        telefono = (request.form.get('telefono') or '').strip()
        nacimiento = (request.form.get('nacimiento') or '').strip()
        direccion = (request.form.get('direccion') or '').strip()
        new_password = (request.form.get('new_password') or '').strip()
        confirm_password = (request.form.get('confirm_password') or '').strip()
        
        # Validaciones
        if not nombres or not email:
            return render_template('ventanas/cuenta.html', usuario=usuario)
        
        # Verificar si el email ya existe (excepto el del usuario actual)
        existing_user = Usuario.query.filter(Usuario.email == email, Usuario.id != usuario.id).first()
        if existing_user:
            return render_template('ventanas/cuenta.html', usuario=usuario)
        
        # Validar contraseñas si se proporcionaron
        if new_password:
            if new_password != confirm_password:
                return render_template('ventanas/cuenta.html', usuario=usuario, error_password='Las contraseñas no coinciden')
            if len(new_password) < 6:
                return render_template('ventanas/cuenta.html', usuario=usuario, error_password='La contraseña debe tener al menos 6 caracteres')
        
        # Actualizar datos del usuario
        usuario.nombres = nombres
        usuario.apellidos = apellidos
        usuario.email = email
        usuario.telefono = telefono
        usuario.direccion = direccion
        
        # Convertir fecha de nacimiento
        if nacimiento:
            try:
                usuario.nacimiento = datetime.strptime(nacimiento, '%Y-%m-%d').date()
            except ValueError:
                return render_template('ventanas/cuenta.html', usuario=usuario)
        
        # Actualizar contraseña si se proporcionó
        if new_password:
            usuario.set_password(new_password)
        
        try:
            db.session.commit()
            session['user_name'] = nombres  # Actualizar nombre en sesión
            # Redirigir para evitar reenvío de formulario y refrescar datos desde la BD
            return redirect(url_for('cuenta'))
        except Exception as e:
            db.session.rollback()
    
    return render_template('ventanas/cuenta.html', usuario=usuario)

@app.route('/contacto.html', methods=['GET', 'POST'])
def contacto():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        mensaje_texto = request.form.get('mensaje')
        
        # Validaciones
        if not nombre or not correo or not mensaje_texto:
            return render_template('ventanas/contacto.html')
        
        # Crear nuevo mensaje
        nuevo_mensaje = Mensaje(
            nombre=nombre,
            correo=correo,
            mensaje=mensaje_texto
        )
        
        try:
            db.session.add(nuevo_mensaje)
            db.session.commit()
            return redirect(url_for('contacto'))
        except Exception as e:
            db.session.rollback()
    
    return render_template('ventanas/contacto.html')

@app.route('/carrito.html')
def carrito():
    # Obtener carrito de la sesión (funciona con o sin login)
    carrito_items = session.get('carrito', [])
    return render_template('ventanas/carrito.html', carrito_items=carrito_items)

@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    # Obtener datos del formulario
    nombre_producto = request.form.get('nombre_producto')
    talla = request.form.get('talla')
    precio = request.form.get('precio', '0')

    if not nombre_producto or not talla:
        return redirect(request.referrer)

    # Inicializar carrito si no existe
    if 'carrito' not in session:
        session['carrito'] = []

    # Agregar producto al carrito
    item = {
        'nombre': nombre_producto,
        'talla': talla,
        'precio': precio
    }

    session['carrito'].append(item)
    session.modified = True

    return redirect(request.referrer)

@app.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
    carrito_items = session.get('carrito', [])
    
    if not carrito_items:
        return redirect(url_for('carrito'))
    
    # Limpiar carrito
    session['carrito'] = []
    session.modified = True
    
    return redirect(url_for('carrito'))

# MARCAS
@app.route('/nike.html')
def nike():
    return render_template('productosNike/nike.html')

@app.route('/adidas.html')
def adidas():
    return render_template('productosAdidas/adidas.html')

@app.route('/newbalance.html')
def newbalance():
    return render_template('productosNewBalance/newbalance.html')

@app.route('/converse.html')
def converse():
    return render_template('productosConverse/converse.html')

@app.route('/vans.html')
def vans():
    return render_template('productosVans/vans.html')

@app.route('/reebok.html')
def reebok():
    return render_template('productosReebok/reebok.html')

# PRODUCTOS 
@app.route('/nikegato.html')
def nikegato():
    producto = Producto.query.filter_by(pagina_html='nikegato.html').first()
    return render_template('productosNike/nikegato.html', producto=producto)

@app.route('/nikeairjordan1mid.html')
def nikeairjordan1mid():
    producto = Producto.query.filter_by(pagina_html='nikeairjordan1mid.html').first()
    return render_template('productosNike/nikeairjordan1mid.html', producto=producto)

@app.route('/nikeairmaxnuaxis.html')
def nikeairmaxnuaxis():
    producto = Producto.query.filter_by(pagina_html='nikeairmaxnuaxis.html').first()
    return render_template('productosNike/nikeairmaxnuaxis.html', producto=producto)

@app.route('/nikep6000.html')
def nikep6000():
    producto = Producto.query.filter_by(pagina_html='nikep6000.html').first()
    return render_template('productosNike/nikep6000.html', producto=producto)

@app.route('/nikepegasusplus.html')
def nikepegasusplus():
    producto = Producto.query.filter_by(pagina_html='nikepegasusplus.html').first()
    return render_template('productosNike/nikepegasusplus.html', producto=producto)

@app.route('/nikepremieriii.html')
def nikepremieriii():
    producto = Producto.query.filter_by(pagina_html='nikepremieriii.html').first()
    return render_template('productosNike/nikepremieriii.html', producto=producto)

@app.route('/adidassamba.html')
def adidassamba():
    producto = Producto.query.filter_by(pagina_html='adidassamba.html').first()
    return render_template('productosAdidas/adidassamba.html', producto=producto)

@app.route('/adidaskaptir.html')
def adidaskaptir():
    producto = Producto.query.filter_by(pagina_html='adidaskaptir.html').first()
    return render_template('productosAdidas/adidaskaptir.html', producto=producto)

@app.route('/adidasadizero.html')
def adidasadizero():
    producto = Producto.query.filter_by(pagina_html='adidasadizero.html').first()
    return render_template('productosAdidas/adidasadizero.html', producto=producto)

@app.route('/adidascampus.html')
def adidascampus():
    producto = Producto.query.filter_by(pagina_html='adidascampus.html').first()
    return render_template('productosAdidas/adidascampus.html', producto=producto)

@app.route('/adidasgazelle.html')
def adidasgazelle():
    producto = Producto.query.filter_by(pagina_html='adidasgazelle.html').first()
    return render_template('productosAdidas/adidasgazelle.html', producto=producto)

@app.route('/adidasultraboost.html')
def adidasultraboost():
    producto = Producto.query.filter_by(pagina_html='adidasultraboost.html').first()
    return render_template('productosAdidas/adidasultraboost.html', producto=producto)

# PRODUCTOS NEW BALANCE
@app.route('/newbalance2002r.html')
def newbalance2002r():
    producto = Producto.query.filter_by(pagina_html='newbalance2002r.html').first()
    return render_template('productosNewBalance/newbalance2002r.html', producto=producto)

@app.route('/newbalance574.html')
def newbalance574():
    producto = Producto.query.filter_by(pagina_html='newbalance574.html').first()
    return render_template('productosNewBalance/newbalance574.html', producto=producto)

@app.route('/newbalance740.html')
def newbalance740():
    producto = Producto.query.filter_by(pagina_html='newbalance740.html').first()
    return render_template('productosNewBalance/newbalance740.html', producto=producto)

@app.route('/newbalance9060.html')
def newbalance9060():
    producto = Producto.query.filter_by(pagina_html='newbalance9060.html').first()
    return render_template('productosNewBalance/newbalance9060.html', producto=producto)

@app.route('/newbalance990v6.html')
def newbalance990v6():
    producto = Producto.query.filter_by(pagina_html='newbalance990v6.html').first()
    return render_template('productosNewBalance/newbalance990v6.html', producto=producto)

@app.route('/newbalance997r.html')
def newbalance997r():
    producto = Producto.query.filter_by(pagina_html='newbalance997r.html').first()
    return render_template('productosNewBalance/newbalance997r.html', producto=producto)

# PRODUCTOS CONVERSE
@app.route('/conversechuck70.html')
def conversechuck70():
    producto = Producto.query.filter_by(pagina_html='conversechuck70.html').first()
    return render_template('productosConverse/conversechuck70.html', producto=producto)

@app.route('/conversechucktaylor.html')
def conversechucktaylor():
    producto = Producto.query.filter_by(pagina_html='conversechucktaylor.html').first()
    return render_template('productosConverse/conversechucktaylor.html', producto=producto)

@app.route('/conversecl98.html')
def conversecl98():
    producto = Producto.query.filter_by(pagina_html='conversecl98.html').first()
    return render_template('productosConverse/conversecl98.html', producto=producto)

@app.route('/conversefastbreak.html')
def conversefastbreak():
    producto = Producto.query.filter_by(pagina_html='conversefastbreak.html').first()
    return render_template('productosConverse/conversefastbreak.html', producto=producto)

@app.route('/converserunstar.html')
def converserunstar():
    producto = Producto.query.filter_by(pagina_html='converserunstar.html').first()
    return render_template('productosConverse/converserunstar.html', producto=producto)

@app.route('/conversewave.html')
def conversewave():
    producto = Producto.query.filter_by(pagina_html='conversewave.html').first()
    return render_template('productosConverse/conversewave.html', producto=producto)

# PRODUCTOS VANS
@app.route('/vanschukka.html')
def vanschukka():
    producto = Producto.query.filter_by(pagina_html='vanschukka.html').first()
    return render_template('productosVans/vanschukka.html', producto=producto)

@app.route('/vansclassicslip.html')
def vansclassicslip():
    producto = Producto.query.filter_by(pagina_html='vansclassicslip.html').first()
    return render_template('productosVans/vansclassicslip.html', producto=producto)

@app.route('/vansoldskool.html')
def vansoldskool():
    producto = Producto.query.filter_by(pagina_html='vansoldskool.html').first()
    return render_template('productosVans/vansoldskool.html', producto=producto)

@app.route('/vanssk8hi.html')
def vanssk8hi():
    producto = Producto.query.filter_by(pagina_html='vanssk8hi.html').first()
    return render_template('productosVans/vanssk8hi.html', producto=producto)

@app.route('/vanssuperlowpro.html')
def vanssuperlowpro():
    producto = Producto.query.filter_by(pagina_html='vanssuperlowpro.html').first()
    return render_template('productosVans/vanssuperlowpro.html', producto=producto)

@app.route('/vansultrarange.html')
def vansultrarange():
    producto = Producto.query.filter_by(pagina_html='vansultrarange.html').first()
    return render_template('productosVans/vansultrarange.html', producto=producto)

# PRODUCTOS REEBOK
@app.route('/reebokclassicnylon.html')
def reebokclassicnylon():
    producto = Producto.query.filter_by(pagina_html='reebokclassicnylon.html').first()
    return render_template('productosReebok/reebokclassicnylon.html', producto=producto)

@app.route('/reebokfiori.html')
def reebokfiori():
    producto = Producto.query.filter_by(pagina_html='reebokfiori.html').first()
    return render_template('productosReebok/reebokfiori.html', producto=producto)

@app.route('/reebokfloatzig.html')
def reebokfloatzig():
    producto = Producto.query.filter_by(pagina_html='reebokfloatzig.html').first()
    return render_template('productosReebok/reebokfloatzig.html', producto=producto)

@app.route('/reeBoknano.html')
def reeBoknano():
    producto = Producto.query.filter_by(pagina_html='reeBoknano.html').first()
    return render_template('productosReebok/reeBoknano.html', producto=producto)

@app.route('/reebokphasecourt.html')
def reebokphasecourt():
    producto = Producto.query.filter_by(pagina_html='reebokphasecourt.html').first()
    return render_template('productosReebok/reebokphasecourt.html', producto=producto)

@app.route('/reebokquestion.html')
def reebokquestion():
    producto = Producto.query.filter_by(pagina_html='reebokquestion.html').first()
    return render_template('productosReebok/reebokquestion.html', producto=producto)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)