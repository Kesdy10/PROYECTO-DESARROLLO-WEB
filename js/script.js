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
