from flask import Flask, render_template, request, jsonify
import sys,os
import my_app.logic.lexico as lexico,my_app.logic.sintactico as sintactico

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/run', methods=['POST'])
def run_logic():
    data = request.json
    result = lexico.lexicoGUI(data)+"---separador---"+sintactico.syntaxGUI(data)  
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)
