from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='templates')

# Ruta para servir archivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)
    
    
# --- Debug endpoints (safe to remove) -------------------------------------
@app.route('/debug/static')
def debug_static():
    """Return JSON with existence info for a provided static file.
    Usage: /debug/static?file=img/encabezado/logo.jpeg
    """
    from flask import request, jsonify
    fn = request.args.get('file')
    if not fn:
        return jsonify({'error': 'missing file parameter'}), 400
    # Normalize path
    safe_path = os.path.normpath(os.path.join(app.static_folder, fn))
    # Ensure path is inside static_dir
    if not safe_path.startswith(app.static_folder):
        return jsonify({'error': 'invalid path'}), 400
    exists = os.path.exists(safe_path)
    return jsonify({'file': fn, 'abs_path': safe_path, 'exists': exists})
    
    
@app.route('/debug/list-static')
def debug_list_static():
    """Return a JSON list of files in the static directory (one level deep).
    Useful to verify Railway has the files checked into the repo.
    """
    from flask import jsonify
    out = []
    for root, dirs, files in os.walk(app.static_folder):
        # only list first level (break after first iteration)
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), app.static_folder)
            out.append(rel.replace('\\\\', '/'))
        break
    return jsonify({'static_root': app.static_folder, 'files': out})
    
# -------------------------------------------------------------------------

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
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)