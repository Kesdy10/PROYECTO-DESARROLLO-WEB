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
    app.run(host='0.0.0.0', port=port, debug=False)