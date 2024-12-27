from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para usar sesiones

# Base de datos ficticia de preguntas
preguntas = [
    {"pregunta": "¿Cuál es tu color favorito?", "opciones": ["Rojo", "Azul", "Verde", "Amarillo"]},
    {"pregunta": "¿Qué mascota prefieres?", "opciones": ["Perro", "Gato", "Ave", "Pez"]},
    {"pregunta": "¿Cuál es tu comida favorita?", "opciones": ["Pizza", "Sushi", "Hamburguesa", "Ensalada"]}
]

# 👉 Ruta de inicio para formulario de datos
@app.route('/')
def index():
    return render_template('index.html')

# 👉 Procesa los datos del formulario y redirige a la primera pregunta
@app.route('/inicio_encuesta', methods=['POST'])
def inicio_encuesta():
    session['nombre'] = request.form.get('nombre')
    session['apellido'] = request.form.get('apellido')
    session['fecha_nacimiento'] = request.form.get('fecha_nacimiento')
    session['email'] = request.form.get('email')
    
    return redirect(url_for('pregunta', numero=1))

# 👉 Muestra cada pregunta de la encuesta
@app.route('/pregunta/<int:numero>')
def pregunta(numero):
    if numero <= len(preguntas):
        return render_template(
            'pregunta.html',
            nombre=session.get('nombre', 'Generador de Encuestas'),
            numero=numero,
            pregunta=preguntas[numero-1]['pregunta'],
            opciones=preguntas[numero-1]['opciones']
        )
    else:
        return render_template('final.html', nombre=session.get('nombre', 'Generador de Encuestas'))

# 👉 Procesa la respuesta de cada pregunta
@app.route('/siguiente/<int:numero>', methods=['POST'])
def siguiente(numero):
    respuesta = request.form.get('respuesta')
    print(f"Pregunta {numero}: {respuesta}")  # Guarda o procesa la respuesta aquí
    
    if numero < len(preguntas):
        return redirect(url_for('pregunta', numero=numero + 1))
    else:
        return redirect(url_for('finalizar'))

# 👉 Página final de agradecimiento
@app.route('/finalizar')
def finalizar():
    return render_template('final.html', nombre=session.get('nombre', 'Generador de Encuestas'))

# 👉 Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
