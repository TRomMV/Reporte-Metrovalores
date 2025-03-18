document.addEventListener("DOMContentLoaded", function () {
    function toggleElements() {
        let isMobile = window.innerWidth <= 768;

        // Mostrar/Ocultar tabla
        document.querySelector(".table-container").style.display = isMobile ? "none" : "block";

        // Mostrar/Ocultar tarjetas y menú hamburguesa
        document.querySelector(".cards-container").style.display = isMobile ? "block" : "none";
        document.querySelector(".hamburger-menu").style.display = isMobile ? "block" : "none";
    }

    // Ejecutar al cargar la página
    toggleElements();

    // Ejecutar cuando se cambia el tamaño de la ventana
    window.addEventListener("resize", toggleElements);
});
