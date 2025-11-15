-Don Gato - Sitio Web de venta de zapatos

Don Gato es una tienda en línea de zapatos que ha ganado popularidad gracias a sus ventas y promociones en redes sociales. La empresa trabaja mediante pago contra entrega, recopilando los datos del cliente después de que los productos son agregados al carrito y se completa el checkout.
Sin embargo, anteriormente la tienda no contaba con un sistema que gestionara eficientemente sus productos, mensajes e información de venta, lo cual generó la necesidad de desarrollar un sistema web completo.


-Explicación del proyecto

El proyecto consiste en la creación de un sitio web para la empresa Don Gato, tienda online dedicada a la venta de zapatos, en donde su método de entrega es pago contra entrega. Esta empresa encarga sus productos por medio de mensajeros, donde se toman datos del cliente y se envían los productos.
Debido a las necesidades sobre la falta de un sistema que recopile productos, mensajes y datos del cliente, se creo el sitio web para la empresa, contando con interfaces y funciones como:

• Login
• Crear usuario
• Olvidaste tu contraseña
• Cuenta
• Formulario de contacto
• Carrito
• Redes sociales
• Interfaz de cada marca que maneja la empresa
• Interfaz de cada producto en stock de la empresa

El sitio web cuenta con diseño responsive, menús dinámicos y contenido multimedia, el cual está dividido en tres fases, las cuales veremos a continuación:

Frontent: Se utilizaron tecnologías para la construcción visual e interactividad del sitio con los siguientes lenguajes:
• HTML para estructura y construcción del sistema.
• CSS para diseño visual de cada ventana con diseño responsive.
• JS para funciones dinámicas y validaciones dentro del sistema.

API: Utilizamos Python con flask para conexión entre el frontent y backend, en donde permite gestionar el flujo de información entre ambas partes, permitiendo que cada función implementada se comunique dentro de la BD.

Backend: Se utiliza la base de datos SQLite para pruebas locales y PostgreSQL para su implementación en la nube. Ambas funcionando en almacenamiento de datos de usuario, formulario de contacto y cada producto del sistema. Esta base de datos ayuda a tener un comprobante al hacer checkout de productos en el carrito, dejándonos ver los datos del usuario, como su nombre, teléfono o dirección, en donde se dirigirá el pedido.


-Alcances

Visualización de marcas y productos:
• Logo de marcas que maneja la empresa
• Nombre del producto
• Precio del producto
• Imágenes de productos
• Tallas en stock
• Botón para agregar al carrito.

Usuarios:
• Registro de usuarios.
• Opción de cambiar contraseña de usuario previamente creado.
• Ver datos de usuario.
• Opción para actualizar datos de usuario.
• Opción para cerrar sesión del usuario previamente logueado.
• Opción para borrar cuenta de usuario

Carrito:
• Nombre y talla de producto agregado.
• Precio del producto
• Cantidad de productos agregados
• Total de un mismo producto, con su precio y la cantidad de veces que aparece.
• Total general de todos los productos agregados

Formulario de contacto y redes sociales:
• Ingreso de nombre, correo y mensaje detallado.
• Integración de redes sociales de la empresa.

General:
• Diseño responsive.
• Menús y funciones dinámicas.
• Comunicación entre frontent y backend mediante API.
• Base de datos tanto local por SQLite como en la nube con PostgreSQL.
• Implementación en la nube mediante la herramienta RailWay.