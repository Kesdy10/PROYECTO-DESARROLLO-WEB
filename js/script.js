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

// ...existing code...

// Simulación de productos en el carrito (puedes reemplazar por datos reales)
let carrito = [
    { nombre: "Croquetas Don Gato", cantidad: 2, precio: 120 },
    { nombre: "Arena Premium", cantidad: 1, precio: 80 }
];

// Función para mostrar productos en la tabla
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

// Función para mostrar el resumen de factura
function mostrarResumen() {
    const total = carrito.reduce((sum, prod) => sum + prod.cantidad * prod.precio, 0);
    const direccion = document.getElementById('direccion').value;
    const telefono = document.getElementById('telefono').value;
    const resumenDiv = document.getElementById('resumen-factura');
    resumenDiv.innerHTML = `
        <strong>Total a pagar:</strong> $${total}<br>
        <strong>Dirección:</strong> ${direccion}<br>
        <strong>Teléfono:</strong> ${telefono}<br>
        <strong>Pago:</strong> Contra entrega
    `;
}

// Actualiza el resumen cuando se cambia la dirección o teléfono
document.getElementById('direccion').addEventListener('input', mostrarResumen);
document.getElementById('telefono').addEventListener('input', mostrarResumen);

// Botón para confirmar pedido
document.getElementById('confirmar-pedido').addEventListener('click', function() {
    mostrarResumen();
    alert('¡Pedido confirmado! Se enviará a la dirección indicada y se paga contra entrega.');
    // Aquí puedes agregar la lógica para enviar el pedido al backend si lo necesitas
});

// Inicializa la vista
mostrarCarrito();
mostrarResumen();

// ...existing code...