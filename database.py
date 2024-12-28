import sqlite3

def init_db():
    conn = sqlite3.connect('encuestas.db')
    cursor = conn.cursor()

    # Tabla para guardar encuestas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS encuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            preguntas TEXT NOT NULL -- Guardaremos las preguntas y opciones como JSON
        )
    ''')

    # Tabla para guardar respuestas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            encuesta_id INTEGER NOT NULL,
            respuestas TEXT NOT NULL, -- Respuestas del usuario como JSON
            FOREIGN KEY (encuesta_id) REFERENCES encuestas (id)
        )
    ''')

    conn.commit()
    conn.close()

# Llama esta función una vez para inicializar la base de datos
init_db()
