function validarOrientacion() {
    const esVertical = window.innerHeight > window.innerWidth;
    const esMovil = window.innerWidth <= 768;

    if (esMovil && esVertical) {
        document.body.innerHTML = `
            <div style="text-align:center; padding:40px; font-size:18px; background-color:#f5f5f5; color:#333;">
                📱 Esta aplicación está diseñada para usarse en <strong>modo horizontal</strong>.<br>
                Por favor gira tu dispositivo.
            </div>
        `;
    }
}

window.addEventListener("load", validarOrientacion);
window.addEventListener("resize", validarOrientacion);
