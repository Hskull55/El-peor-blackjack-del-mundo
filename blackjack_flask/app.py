from flask import Flask, render_template, session, redirect, request, json

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

victorias = 0
derrotas = 0
empates = 0

stats = {'gamesWon': 0, 'gamesLost': 0, 'gamesTied': 0}


def actualizar_estadisticas(resultado):
    global victorias, derrotas, empates

    if resultado == 'victoria':
        victorias += 1
    elif resultado == 'derrota':
        derrotas += 1
    elif resultado == 'empate':
        empates += 1

def cargar_traducciones(idioma):
    with open(f'traducciones/{idioma}.json', 'r', encoding='utf-8') as archivo:
        return json.load(archivo)


@app.route('/')
def index():
    idioma = session.get('idioma', 'es')  # Por defecto, usa español
    traducciones = cargar_traducciones(idioma)
    return render_template('index.html', traducciones=traducciones)

@app.route('/play')
def play():
    idioma = session.get('idioma', 'es')  # Por defecto, usa español
    traducciones = cargar_traducciones(idioma)
    return render_template('game.html', traducciones=traducciones)

@app.route('/settings')
def settings():
    idioma = session.get('idioma', 'es')  # Por defecto, usa español
    traducciones = cargar_traducciones(idioma)
    return render_template('settings.html', traducciones=traducciones)

@app.route('/stats')
def stats():
    idioma = session.get('idioma', 'es')  # Por defecto, usa español
    traducciones = cargar_traducciones(idioma)
    return render_template('stats.html', traducciones=traducciones)

@app.route('/cambiar_idioma/<idioma>')
def cambiar_idioma(idioma):
    session['idioma'] = idioma
    print(session['idioma'])  # Agregar esta línea para verificar
    return json.dumps({'success': True}), 200, {'ContentType':'application/json'}


@app.route('/obtener_estadisticas')
def obtener_estadisticas():
    # Aquí es donde deberías obtener tus estadísticas
    # Puedes tener una variable o función que las recoja y las devuelva como un diccionario
    # Por ejemplo, si las tienes en una variable stats, podrías hacer algo como:
    # stats = {'gamesWon': 10, 'gamesLost': 5, 'gamesTied': 2}
    # Luego, la retornas como una respuesta JSON
    stats = {'gamesWon': 10, 'gamesLost': 5, 'gamesTied': 2}
    return json.dumps(stats), 200, {'ContentType':'application/json'}

@app.route('/actualizar_estadisticas', methods=['POST'])
def actualizar_estadisticas():
    resultado = request.json['resultado']

    # Aquí deberías tener un mecanismo para actualizar las estadísticas
    # Esto podría ser una base de datos, un archivo, etc.
    # Ejemplo básico usando una variable global (que no es recomendado para producción)
    if 'stats' not in session:
        session['stats'] = {'gamesWon': 0, 'gamesLost': 0, 'gamesTied': 0}

    if resultado == 'jugador':
        session['stats']['gamesWon'] += 1
    elif resultado == 'crupier':
        session['stats']['gamesLost'] += 1
    elif resultado == 'empate':
        session['stats']['gamesTied'] += 1

    return json.dumps({'success': True, 'stats': session['stats']}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)
