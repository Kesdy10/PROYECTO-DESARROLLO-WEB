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
});