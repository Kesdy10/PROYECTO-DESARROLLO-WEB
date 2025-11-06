// Contraseña: función legacy por compatibilidad
function togglePassword() {
    var input = document.getElementById("contrasena");
    if (!input) return;
    input.type = (input.type === "password") ? "text" : "password";
}

// Inicializaciones ligeras y sin dependencias del DOM
document.addEventListener('DOMContentLoaded', function() {
    // Botones de selección (simple highlight)
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

    // Checkboxes con data-toggle para mostrar/ocultar contraseñas
    document.querySelectorAll('[data-toggle]').forEach(cb => {
        const targetId = cb.getAttribute('data-toggle');
        cb.addEventListener('change', () => {
            const input = document.getElementById(targetId);
            if (!input) return;
            input.type = cb.checked ? 'text' : 'password';
        });
    });
});