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