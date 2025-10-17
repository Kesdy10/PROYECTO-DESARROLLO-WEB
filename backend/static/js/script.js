//Contraseña
function togglePassword() {
    var input = document.getElementById("contrasena");
    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}

const botones = document.querySelectorAll(".datos-producto button");
botones.forEach(boton => {
    boton.addEventListener("click", () => {
        botones.forEach(b => {
            b.classList.remove("activo");
            b.style.backgroundColor = "";
            b.style.color = "";
        });

        boton.classList.add("activo");
        boton.style.backgroundColor = "yellowgreen";
        boton.style.color = "white";
    });
});

function mostrarCarrito() {
    const tbody = document.getElementById('carrito-productos');
    tbody.innerHTML = '';
    carrito.forEach(producto => {
        const subtotal = producto.cantidad * producto.precio;
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${producto.nombre}</td>
            <td>${producto.cantidad}</td>
            <td>$${producto.precio}</td>
            <td>$${subtotal}</td>
        `;
        tbody.appendChild(fila);
    });
}

function mostrarResumen() {
    const total = carrito.reduce((sum, prod) => sum + prod.cantidad * prod.precio, 0);
    const direccion = document.getElementById('direccion').value;
    const telefono = document.getElementById('telefono').value;
    const resumenDiv = document.getElementById('resumen-factura');
    resumenDiv.innerHTML = `
        <strong>Total a pagar:</strong> $${total}<br>
        <strong>Direccion:</strong> ${direccion}<br>
        <strong>Telefono:</strong> ${telefono}<br>
        <strong>Pago:</strong> Contra entrega
    `;
}

document.getElementById('direccion').addEventListener('input', mostrarResumen);
document.getElementById('telefono').addEventListener('input', mostrarResumen);
document.getElementById('confirmar-pedido').addEventListener('click', function() {
    mostrarResumen();
    alert('Pedido confirmado! Se enviara a la direccion del usuario y su metodo de pago es pago contra entrega.');

});

mostrarCarrito();
mostrarResumen();

// Funcionalidad del carrusel de imágenes
function inicializarCarrusel() {
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
    
    // Event listeners para botones del carrusel
    const btnAnterior = document.querySelector('.carrusel-anterior');
    const btnSiguiente = document.querySelector('.carrusel-siguiente');
    
    if (btnAnterior) btnAnterior.onclick = anterior;
    if (btnSiguiente) btnSiguiente.onclick = siguiente;
    
    // Event listeners para teclas de navegación
    document.addEventListener('keydown', function(e) {
        if (e.key === "ArrowLeft") anterior();
        if (e.key === "ArrowRight") siguiente();
    });
}

// Funcionalidad de selección de tallas y carrito
function inicializarTallas() {
    const tallas = document.querySelectorAll('.talla-item');
    const btnAgregar = document.getElementById('agregar-carrito');
    let tallaSeleccionada = null;

    tallas.forEach(talla => {
        talla.addEventListener('click', () => {
            tallas.forEach(t => t.classList.remove('selected'));
            talla.classList.add('selected');
            tallaSeleccionada = talla.dataset.talla;
            btnAgregar.disabled = false;
            btnAgregar.classList.add('enabled');
        });
    });

    btnAgregar.addEventListener('click', () => {
        if (tallaSeleccionada) {
            // Obtener información del producto desde el DOM
            const nombreProducto = document.querySelector('.titulo-producto').textContent;
            const precioTexto = document.querySelector('.precio-producto').textContent;
            const precio = parseInt(precioTexto.replace('Q', ''));
            
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

// Inicializar todas las funcionalidades cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    inicializarCarrusel();
    inicializarTallas();
});