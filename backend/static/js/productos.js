document.addEventListener('DOMContentLoaded', function() {
    const carruselImagenes = document.querySelector('.carrusel-imagenes');
    if (!carruselImagenes) return;
    
    //Carrusel
    const imagenes = document.querySelectorAll('.carrusel-imagenes img');
    let indice = 0;
    
    function mostrarImagen(idx) {
        imagenes.forEach((img, i) => {
            img.classList.toggle('active', i === idx);
        });
    }
    
    function anterior() {
        indice = (indice - 1 + imagenes.length) % imagenes.length;
        mostrarImagen(indice);
    }
    
    function siguiente() {
        indice = (indice + 1) % imagenes.length;
        mostrarImagen(indice);
    }
    
    // IZQUIERDA Y DERECHA
    const btnAnterior = document.querySelector('.carrusel-anterior');
    const btnSiguiente = document.querySelector('.carrusel-siguiente');
    
    if (btnAnterior) btnAnterior.onclick = anterior;
    if (btnSiguiente) btnSiguiente.onclick = siguiente;
    
    //Teclas
    document.addEventListener('keydown', function(e) {
        if (e.key === "ArrowLeft") anterior();
        if (e.key === "ArrowRight") siguiente();
    });

    //Tallas
    const tallas = document.querySelectorAll('.talla-item');
    const btnAgregar = document.getElementById('agregar-carrito');
    let tallaSeleccionada = null;

    tallas.forEach(talla => {
        talla.addEventListener('click', () => {
            tallas.forEach(t => t.classList.remove('selected'));
            talla.classList.add('selected');
            tallaSeleccionada = talla.dataset.talla;
            if (btnAgregar) {
                btnAgregar.disabled = false;
                btnAgregar.classList.add('enabled');
            }
        });
    });

    if (btnAgregar) {
        btnAgregar.addEventListener('click', () => {
            if (tallaSeleccionada) {
                // Obtener información del producto desde el DOM
                const nombreProducto = document.querySelector('.titulo-producto')?.textContent || 'Producto';
                const precioTexto = document.querySelector('.precio-producto')?.textContent || 'Q0';
                const precio = parseInt(precioTexto.replace('Q', '')) || 0;
                
                let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
                carrito.push({
                    producto: nombreProducto,
                    talla: tallaSeleccionada,
                    precio: precio
                });
                localStorage.setItem('carrito', JSON.stringify(carrito));
                alert(`Agregado al carrito: ${nombreProducto}, Talla ${tallaSeleccionada}`);
            }
        });
    }
});