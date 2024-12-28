import sqlite3
import json
import qrcode
import base64
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para usar sesiones

app.config['MAIL_SERVER'] = 'smtp.tu_servidor.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'tu_correo@example.com'
app.config['MAIL_PASSWORD'] = 'tu_password'
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

def enviar_respuestas(email, respuestas):
    msg = Message('Respuestas de tu encuesta', sender='tu_correo@example.com', recipients=[email])
    msg.body = f"Aquí están las respuestas recibidas:\n\n{respuestas}"
    mail.send(msg)

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

# 👉 Página para generar QR
@app.route('/generar_qr')
def generar_qr():
    return render_template('generar_qr.html')


# 👉 Procesar QR
@app.route('/procesar_qr', methods=['POST'])
def procesar_qr():
    nombre = request.form.get('nombre')
    email = request.form.get('email')

    preguntas = []
    for i in range(1, 6):
        pregunta = request.form.get(f'pregunta_{i}')
        if pregunta:
            opciones = [
                request.form.get(f'pregunta_{i}_opcion_1'),
                request.form.get(f'pregunta_{i}_opcion_2'),
                request.form.get(f'pregunta_{i}_opcion_3'),
                request.form.get(f'pregunta_{i}_opcion_4'),
            ]
            preguntas.append({"pregunta": pregunta, "opciones": opciones})

    # Guardar encuesta en la base de datos
    conn = sqlite3.connect('encuestas.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO encuestas (nombre, email, preguntas)
        VALUES (?, ?, ?)
    ''', (nombre, email, json.dumps(preguntas)))

    encuesta_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Generar la URL de la encuesta
    url = f"http://127.0.0.1:5000/encuesta/{encuesta_id}"

    # Generar el QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    # Convertir el QR a base64 para enviarlo como imagen al HTML
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Renderizar la página con el QR
    return render_template('qr_result.html', qr_code=qr_base64, url=url)

@app.route('/encuesta/<int:id>', methods=['GET', 'POST'])
def encuesta(id):
    conn = sqlite3.connect('encuestas.db')
    cursor = conn.cursor()

    cursor.execute('SELECT preguntas FROM encuestas WHERE id = ?', (id,))
    data = cursor.fetchone()

    if not data:
        return "Encuesta no encontrada.", 404

    preguntas = json.loads(data[0])

    if request.method == 'POST':
        respuestas = request.form.to_dict()
        cursor.execute('''
            INSERT INTO respuestas (encuesta_id, respuestas)
            VALUES (?, ?)
        ''', (id, json.dumps(respuestas)))

        conn.commit()
        conn.close()

        return "¡Gracias por responder la encuesta!"

    conn.close()
    return render_template('encuesta.html', preguntas=preguntas)


# 👉 Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
