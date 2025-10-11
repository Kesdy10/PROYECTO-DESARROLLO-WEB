from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Prevenir caché en desarrollo
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Ruta para servir archivos estáticos explícitamente
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# VENTANAS
@app.route('/')
def home():
    return render_template('ventanas/login.html')

@app.route('/login.html')
def login_page():
    return render_template('ventanas/login.html')

@app.route('/crearCuenta.html')
def crear_cuenta():
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

# MARCAS
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

# PRODUCTOS 
@app.route('/nikegato.html')
def nikegato():
    return render_template('productosNike/nikegato.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)