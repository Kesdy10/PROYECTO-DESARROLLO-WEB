// Manejador genérico de mensajes de página y confirmación de pedido
(function(){
  document.addEventListener('DOMContentLoaded', function(){
    // Mensajes de página (éxito / error / redirección opcional)
    const holder = document.getElementById('mensajes-pagina');
    if (holder) {
      const err = holder.dataset.error || '';
      const ok = holder.dataset.exito || '';
      const redirect = holder.dataset.redirigir || '';
      if (err) {
        alert(err);
      } else if (ok) {
        if (redirect) {
          if (confirm(ok + "\n\n¿Deseas ir ahora?")) {
            window.location.href = redirect;
          }
        } else {
          alert(ok);
        }
      }
    }

    // Confirmación del carrito
    const btn = document.getElementById('btnConfirmarPedido');
    const form = document.getElementById('formConfirmar');
    const userBox = document.getElementById('datos-envio');
    if (btn && form && userBox) {
      btn.addEventListener('click', function(){
        const hasUser = userBox.dataset.tieneUsuario === '1';
        if (!hasUser) {
          const loginUrl = userBox.dataset.urlLogin || '/login.html';
          alert('Debes iniciar sesión para confirmar tu pedido');
          window.location.href = loginUrl;
          return;
        }
        const dir = userBox.dataset.direccion || 'No especificada';
        const nom = userBox.dataset.nombre || '';
        const cor = userBox.dataset.correo || '';
        const tel = userBox.dataset.telefono || 'No especificado';
        const mensaje = `Se enviará a:\n\nDirección: ${dir}\n\nNombre: ${nom}\nCorreo: ${cor}\nTeléfono: ${tel}`;
        if (confirm(mensaje + "\n\n¿Deseas confirmar el pedido?")) {
          form.submit();
        }
      });
    }
  });
})();
