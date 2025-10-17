from flask import Flask, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

# VENTANAS
@app.route('/')
def login():
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
    return render_template('productosNike/nike.html')

@app.route('/adidas.html')
def adidas():
    return render_template('productosAdidas/adidas.html')

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

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)