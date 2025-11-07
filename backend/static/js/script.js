//TALLAS ACTIVACION
document.addEventListener('DOMContentLoaded', function() {
    const botones = document.querySelectorAll('.datos-producto button');
    if (botones.length) {
        botones.forEach(boton => {
            boton.addEventListener('click', () => {
                botones.forEach(b => {
                    b.classList.remove('activo');
                    b.style.backgroundColor = '';
                    b.style.color = '';
                });
                boton.classList.add('activo');
                boton.style.backgroundColor = 'yellowgreen';
                boton.style.color = 'white';
            });
        });
    }

    // CHECKBOX CONTRASEÑA
    document.querySelectorAll('[data-toggle]').forEach(cb => {
        const targetId = cb.getAttribute('data-toggle');
        cb.addEventListener('change', () => {
            const input = document.getElementById(targetId);
            if (!input) return;
            input.type = cb.checked ? 'text' : 'password';
        });
    });

    // CONFIRMACION BORRAR CUENTA
    const linkBorrarCuenta = document.querySelector('a[href*="borrar_cuenta"]');
    if (linkBorrarCuenta) {
        linkBorrarCuenta.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('¿Estás seguro de que deseas borrar tu cuenta?\n\nEsta accion no se puede deshacer.')) {
                window.location.href = this.href;
            }
        });
    }
});