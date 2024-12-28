let contadorPreguntas = 1;

document.getElementById('agregar-pregunta').addEventListener('click', function () {
    if (contadorPreguntas >= 5) {
        alert('⚠️ Solo puedes agregar un máximo de 5 preguntas.');
        return;
    }

    contadorPreguntas++;

    const preguntasContainer = document.getElementById('preguntas-container');
    const nuevaPregunta = document.createElement('div');
    nuevaPregunta.className = 'pregunta';

    nuevaPregunta.innerHTML = `
        <label for="pregunta_${contadorPreguntas}">Pregunta ${contadorPreguntas}:</label>
        <input type="text" id="pregunta_${contadorPreguntas}" name="pregunta_${contadorPreguntas}" required>

        <div class="opciones">
            <label>Opción 1:</label>
            <input type="text" name="pregunta_${contadorPreguntas}_opcion_1" required>
            <label>Opción 2:</label>
            <input type="text" name="pregunta_${contadorPreguntas}_opcion_2" required>
            <label>Opción 3:</label>
            <input type="text" name="pregunta_${contadorPreguntas}_opcion_3" required>
            <label>Opción 4:</label>
            <input type="text" name="pregunta_${contadorPreguntas}_opcion_4" required>
        </div>
    `;

    preguntasContainer.appendChild(nuevaPregunta);
});
