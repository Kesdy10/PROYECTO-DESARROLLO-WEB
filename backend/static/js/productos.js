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
            
            // Actualizar el campo hidden del formulario
            const tallaInput = document.getElementById('talla-seleccionada');
            if (tallaInput) {
                tallaInput.value = tallaSeleccionada;
            }
            
            if (btnAgregar) {
                btnAgregar.disabled = false;
                btnAgregar.classList.add('enabled');
            }
        });
    });

    // El formulario se envía automáticamente cuando se hace clic en "Agregar al carrito"
    // Ya no necesitamos el event listener del botón porque es un submit button
});