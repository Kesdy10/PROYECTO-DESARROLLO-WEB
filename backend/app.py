from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import inspect
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuración de la base de datos
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura_para_railway_2024'  

# Configurar base de datos PostgreSQL para Railway
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Arreglar el protocolo si es necesario (Railway a veces usa postgres:// en lugar de postgresql://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"✅ Conectando a PostgreSQL: {database_url[:30]}...")
else:
    print("❌ No se encontró DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:default@localhost/default'

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

# Inicializar la base de datos con manejo de errores
def init_database():
    try:
        with app.app_context():
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
            return True
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        return False

# Intentar inicializar la base de datos
init_database()

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

@app.route('/')
def login():
    return render_template('ventanas/login.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nombres + ' ' + (usuario.apellidos or '')
            flash('¡Bienvenido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('ventanas/login.html')

@app.route('/crearCuenta.html', methods=['GET', 'POST'])
def crear_cuenta():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form.get('apellidos', '')
        email = request.form['email']
        telefono = request.form.get('telefono', '')
        nacimiento = request.form.get('nacimiento')
        direccion = request.form.get('direccion', '')
        password = request.form['password']
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('Este email ya está registrado', 'error')
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
            from datetime import datetime
            nuevo_usuario.nacimiento = datetime.strptime(nacimiento, '%Y-%m-%d').date()
        
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Cuenta creada exitosamente. ¡Ahora puedes iniciar sesión!', 'success')
        return redirect(url_for('login_page'))
    
    return render_template('ventanas/crearCuenta.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login_page'))

@app.route('/index.html')
def index():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero', 'error')
        return redirect(url_for('login_page'))
    return render_template('ventanas/index.html')

@app.route('/cuenta.html', methods=['GET', 'POST'])
def cuenta():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero', 'error')
        return redirect(url_for('login_page'))
    
    usuario = Usuario.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        nacimiento = request.form.get('nacimiento')
        direccion = request.form.get('direccion')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones
        if not nombres or not email:
            flash('Los campos Nombres y Correo son obligatorios', 'error')
            return render_template('ventanas/cuenta.html', usuario=usuario)
        
        # Verificar si el email ya existe (excepto el del usuario actual)
        existing_user = Usuario.query.filter(Usuario.email == email, Usuario.id != usuario.id).first()
        if existing_user:
            flash('Este correo ya está registrado por otro usuario', 'error')
            return render_template('ventanas/cuenta.html', usuario=usuario)
        
        # Validar contraseñas si se proporcionaron
        if new_password:
            if new_password != confirm_password:
                flash('Las contraseñas no coinciden', 'error')
                return render_template('ventanas/cuenta.html', usuario=usuario)
            if len(new_password) < 6:
                flash('La contraseña debe tener al menos 6 caracteres', 'error')
                return render_template('ventanas/cuenta.html', usuario=usuario)
        
        # Actualizar datos del usuario
        usuario.nombres = nombres
        usuario.apellidos = apellidos
        usuario.email = email
        usuario.telefono = telefono
        usuario.direccion = direccion
        
        # Convertir fecha de nacimiento
        if nacimiento:
            try:
                from datetime import datetime
                usuario.nacimiento = datetime.strptime(nacimiento, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha inválido', 'error')
                return render_template('ventanas/cuenta.html', usuario=usuario)
        
        # Actualizar contraseña si se proporcionó
        if new_password:
            usuario.set_password(new_password)
        
        try:
            db.session.commit()
            session['user_name'] = nombres  # Actualizar nombre en sesión
            flash('Datos actualizados exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar los datos', 'error')
    
    return render_template('ventanas/cuenta.html', usuario=usuario)

@app.route('/contacto.html', methods=['GET', 'POST'])
def contacto():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero', 'error')
        return redirect(url_for('login_page'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        mensaje_texto = request.form.get('mensaje')
        
        # Validaciones
        if not nombre or not correo or not mensaje_texto:
            flash('Todos los campos son obligatorios', 'error')
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
            flash('¡Mensaje enviado exitosamente! Te contactaremos pronto.', 'success')
            return redirect(url_for('contacto'))
        except Exception as e:
            db.session.rollback()
            flash('Error al enviar el mensaje. Inténtalo de nuevo.', 'error')
    
    return render_template('ventanas/contacto.html')

@app.route('/carrito.html')
def carrito():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero', 'error')
        return redirect(url_for('login_page'))
    return render_template('ventanas/carrito.html')

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
    return render_template('productosNike/nikegato.html')

@app.route('/nikeairjordan1mid.html')
def nikeairjordan1mid():
    return render_template('productosNike/nikeairjordan1mid.html')

@app.route('/nikeairmaxnuaxis.html')
def nikeairmaxnuaxis():
    return render_template('productosNike/nikeairmaxnuaxis.html')

@app.route('/nikep6000.html')
def nikep6000():
    return render_template('productosNike/nikep6000.html')

@app.route('/nikepegasusplus.html')
def nikepegasusplus():
    return render_template('productosNike/nikepegasusplus.html')

@app.route('/nikepremieriii.html')
def nikepremieriii():
    return render_template('productosNike/nikepremieriii.html')

@app.route('/adidassamba.html')
def adidassamba():
    return render_template('productosAdidas/adidassamba.html')

@app.route('/adidaskaptir.html')
def adidaskaptir():
    return render_template('productosAdidas/adidaskaptir.html')

@app.route('/adidasadizero.html')
def adidasadizero():
    return render_template('productosAdidas/adidasadizero.html')

@app.route('/adidascampus.html')
def adidascampus():
    return render_template('productosAdidas/adidascampus.html')

@app.route('/adidasgazelle.html')
def adidasgazelle():
    return render_template('productosAdidas/adidasgazelle.html')

@app.route('/adidasultraboost.html')
def adidasultraboost():
    return render_template('productosAdidas/adidasultraboost.html')

# PRODUCTOS NEW BALANCE
@app.route('/newbalance2002r.html')
def newbalance2002r():
    return render_template('productosNewBalance/newbalance2002r.html')

@app.route('/newbalance574.html')
def newbalance574():
    return render_template('productosNewBalance/newbalance574.html')

@app.route('/newbalance740.html')
def newbalance740():
    return render_template('productosNewBalance/newbalance740.html')

@app.route('/newbalance9060.html')
def newbalance9060():
    return render_template('productosNewBalance/newbalance9060.html')

@app.route('/newbalance990v6.html')
def newbalance990v6():
    return render_template('productosNewBalance/newbalance990v6.html')

@app.route('/newbalance997r.html')
def newbalance997r():
    return render_template('productosNewBalance/newbalance997r.html')

# PRODUCTOS CONVERSE
@app.route('/conversechuck70.html')
def conversechuck70():
    return render_template('productosConverse/conversechuck70.html')

@app.route('/conversechucktaylor.html')
def conversechucktaylor():
    return render_template('productosConverse/conversechucktaylor.html')

@app.route('/conversecl98.html')
def conversecl98():
    return render_template('productosConverse/conversecl98.html')

@app.route('/conversefastbreak.html')
def conversefastbreak():
    return render_template('productosConverse/conversefastbreak.html')

@app.route('/converserunstar.html')
def converserunstar():
    return render_template('productosConverse/converserunstar.html')

@app.route('/conversewave.html')
def conversewave():
    return render_template('productosConverse/conversewave.html')

# PRODUCTOS VANS
@app.route('/vanschukka.html')
def vanschukka():
    return render_template('productosVans/vanschukka.html')

@app.route('/vansclassicslip.html')
def vansclassicslip():
    return render_template('productosVans/vansclassicslip.html')

@app.route('/vansoldskool.html')
def vansoldskool():
    return render_template('productosVans/vansoldskool.html')

@app.route('/vanssk8hi.html')
def vanssk8hi():
    return render_template('productosVans/vanssk8hi.html')

@app.route('/vanssuperlowpro.html')
def vanssuperlowpro():
    return render_template('productosVans/vanssuperlowpro.html')

@app.route('/vansultrarange.html')
def vansultrarange():
    return render_template('productosVans/vansultrarange.html')

# PRODUCTOS REEBOK
@app.route('/reebokclassicnylon.html')
def reebokclassicnylon():
    return render_template('productosReebok/reebokclassicnylon.html')

@app.route('/reebokfiori.html')
def reebokfiori():
    return render_template('productosReebok/reebokfiori.html')

@app.route('/reebokfloatzig.html')
def reebokfloatzig():
    return render_template('productosReebok/reebokfloatzig.html')

@app.route('/reeBoknano.html')
def reeBoknano():
    return render_template('productosReebok/reeBoknano.html')

@app.route('/reebokphasecourt.html')
def reebokphasecourt():
    return render_template('productosReebok/reebokphasecourt.html')

@app.route('/reebokquestion.html')
def reebokquestion():
    return render_template('productosReebok/reebokquestion.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    
    # En desarrollo, usar el servidor de desarrollo de Flask
    # En producción, Railway usará Gunicorn
    app.run(host='0.0.0.0', port=port, debug=False)