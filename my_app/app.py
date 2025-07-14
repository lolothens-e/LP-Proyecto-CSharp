from flask import Flask, render_template, request, jsonify
import sys
import os

# Añade la ruta del proyecto al sys.path para que Flask encuentre los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos SOLO la nueva función de análisis
from logic.sintactico import analizar_codigo 

app = Flask(__name__)

@app.route('/')
def home():
    """ Sirve la página principal de la aplicación. """
    return render_template('index.html')  

@app.route('/run', methods=['POST'])
def run_logic():
    """ Recibe el código, lo analiza y devuelve los resultados en JSON. """
    # 1. Obtener el código enviado desde el frontend
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({'errors': ['No se recibió código para analizar.']}), 400
    
    codigo = data.get('input', '')

    # 2. Llamar a nuestra función centralizada de análisis
    resultados = analizar_codigo(codigo)
    
    # 3. Formatear la respuesta para el frontend
    response = {
        'lexical_tokens': resultados.get('tokens', []),
        'errors': resultados.get('errors', [])
    }
    
    # 4. Devolver los resultados como JSON
    return jsonify(response)

if __name__ == '__main__':
    # El modo debug es útil para desarrollo, se recarga con cada cambio.
    app.run(debug=True, port=5000)