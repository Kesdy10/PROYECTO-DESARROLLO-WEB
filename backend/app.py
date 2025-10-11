from flask import Flask, render_template

app = Flask(__name__)

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
    app.run(debug=True)