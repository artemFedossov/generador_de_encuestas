from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Base de datos ficticia de preguntas
preguntas = [
    {"pregunta": "¿Cuál es tu color favorito?", "opciones": ["Rojo", "Azul", "Verde", "Amarillo"]},
    {"pregunta": "¿Qué mascota prefieres?", "opciones": ["Perro", "Gato", "Ave", "Pez"]},
    {"pregunta": "¿Cuál es tu comida favorita?", "opciones": ["Pizza", "Sushi", "Hamburguesa", "Ensalada"]}
]

@app.route('/')
def inicio():
    return redirect(url_for('pregunta', numero=1))

@app.route('/pregunta/<int:numero>')
def pregunta(numero):
    if numero <= len(preguntas):
        return render_template(
            'pregunta.html',
            nombre='',
            numero=numero,
            pregunta=preguntas[numero-1]['pregunta'],
            opciones=preguntas[numero-1]['opciones']
        )
    else:
        return render_template('final.html', nombre='Mi Empresa')

@app.route('/siguiente/<int:numero>', methods=['POST'])
def siguiente(numero):
    respuesta = request.form.get('respuesta')
    print(f"Pregunta {numero}: {respuesta}")  # Guarda o procesa la respuesta aquí
    
    if numero < len(preguntas):
        return redirect(url_for('pregunta', numero=numero + 1))
    else:
        return redirect(url_for('finalizar'))

@app.route('/finalizar')
def finalizar():
    return render_template('final.html', nombre='Mi Empresa')

if __name__ == '__main__':
    app.run(debug=True)
