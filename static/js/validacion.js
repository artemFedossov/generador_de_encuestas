function validarSeleccion() {
    const opciones = document.querySelectorAll('input[name="respuesta"]');
    for (let opcion of opciones) {
        if (opcion.checked) {
            return true; // Si alguna está marcada, el formulario se envía.
        }
    }
    alert('⚠️ Por favor, selecciona una opción antes de continuar.');
    return false; // Evita que el formulario se envíe.
}
