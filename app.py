import sqlite3
import json
import qrcode
from flask import Flask, render_template, request, redirect, url_for, session
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para usar sesiones

def guardar_encuesta():
    conn = sqlite3.connect('encuestas.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO encuestas (preguntas) VALUES (?)', (json.dumps(preguntas),))
    conn.commit()
    encuesta_id = cursor.lastrowid
    conn.close()
    return encuesta_id

preguntas = [
    {"pregunta": "¿Cuál es tu color favorito?", "opciones": ["Rojo", "Azul", "Verde", "Amarillo"]},
    {"pregunta": "¿Qué mascota prefieres?", "opciones": ["Perro", "Gato", "Ave", "Pez"]},
    {"pregunta": "¿Cuál es tu comida favorita?", "opciones": ["Pizza", "Sushi", "Hamburguesa", "Ensalada"]}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicio/<int:id>', methods=['GET', 'POST'])
def inicio(id):
    if request.method == 'POST':
        session['nombre'] = request.form.get('nombre')
        session['apellido'] = request.form.get('apellido')
        session['fecha_nacimiento'] = request.form.get('fecha_nacimiento')
        session['email'] = request.form.get('email')
        return redirect(url_for('encuesta', id=id))

    return render_template('index.html', encuesta_id=id)

@app.route('/generar_qr')
def generar_qr():
    encuesta_id = guardar_encuesta()
    url = f"http://127.0.0.1:5000/inicio/{encuesta_id}"

    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('static/qr.png')

    return f"QR generado: <img src='/static/qr.png'>"

@app.route('/encuesta/<int:id>', methods=['GET', 'POST'])
def guardar_encuesta():
    conn = sqlite3.connect('encuestas.db')
    cursor = conn.cursor()

    # Inserta un nombre ficticio o dinámico para la encuesta
    nombre_encuesta = "Encuesta Generada"  # Puedes cambiar esto según sea necesario

    cursor.execute(
        'INSERT INTO encuestas (nombre, preguntas) VALUES (?, ?)',
        (nombre_encuesta, json.dumps(preguntas))
    )
    conn.commit()
    encuesta_id = cursor.lastrowid
    conn.close()
    return encuesta_id

if __name__ == '__main__':
    app.run(debug=True)
