import ply.yacc as yacc, datetime
from my_app.logic.lexico import tokens

#lacedeno11 aporte inicio

# PRECEDENCIA DE OPERADORES
# Define el orden y la asociatividad de los operadores para resolver ambigüedades.
# Se lista de MENOR a MAYOR precedencia.
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'IGUAL', 'DIFERENTE'), # nonassoc significa que no se pueden encadenar (ej: a < b < c)
    ('nonassoc', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIR', 'MODULO'),
    ('right', 'NOT'), # right asociativo
    ('right', 'UMINUS'),  # Operador unario para números negativos (ej: -5)
)


#lacedeno11 aporte fin
symbol_table = {}
#Lacedeno11 aporte inicio

# --- ESTRUCTURAS PARA EL ANÁLISIS SEMÁNTICO ---

# 1. Contexto: Nos ayuda a saber dónde estamos (dentro de un bucle, función, etc.)
semantic_context = {
    'dentro_de_bucle': 0,
    'funcion_actual': None # Guardará el nombre de la función que se está analizando
}

# 2. Lista de Errores: Acumularemos todos los errores semánticos aquí.
errores_semanticos = []

# --- FUNCIONES AUXILIARES PARA SEMÁNTICA ---

def registrar_error_semantico(mensaje, linea):
    """Función para registrar y mostrar un error semántico."""
    error = f"[Error Semántico] Línea {linea}: {mensaje}"
    errores_semanticos.append(error)

def get_expression_type(node):
    if isinstance(node, int): return 'int'
    if isinstance(node, float): return 'float'
    if isinstance(node, str):
        if node == 'true' or node == 'false': return 'bool'
        if node.startswith('"') and node.endswith('"'): return 'string'
        if node in symbol_table:
            if symbol_table[node].get('type') != 'function':
                return symbol_table[node].get('type')
            else:
                return 'desconocido'
        else:
            registrar_error_semantico(f"La variable '{node}' no ha sido declarada.", 0)
            return 'desconocido'
    if isinstance(node, tuple):
        op = node[0]
        if op in ('+', '-', '*', '/', '%'):
            return get_expression_type(node[1])
        if op in ('<', '>', '<=', '>=', '==', '!=', '&&', '||', '!'):
            return 'bool'
        if op == 'nueva_lista':
            tipo_interno = node[1].split('<')[1].rstrip('>')
            return f"List<{tipo_interno}>"
        if op == 'nuevo_array':
            tipo_array = node[1].split()[1]
            return f"{tipo_array}[]"
        return 'desconocido'


# --- REGLA PARA RETURN ---
# AÑADE ESTA NUEVA FUNCIÓN
def p_instruccion_return(p):
    'instruccion_return : RETURN expresion'
    
    # --- SEMÁNTICA: Validar el tipo de retorno ---
    funcion_actual = semantic_context['funcion_actual']
    if funcion_actual is None:
        registrar_error_semantico("'return' solo puede usarse dentro de una función.", p.lineno(1))
    else:
        # Se comprueba si la función existe en la tabla de símbolos para evitar errores
        if funcion_actual in symbol_table:
            tipo_esperado = symbol_table[funcion_actual]['return_type']
            tipo_retornado = get_expression_type(p[2])
            
            if tipo_esperado == 'void':
                 registrar_error_semantico(f"La función '{funcion_actual}' es de tipo 'void' y no puede retornar un valor.", p.lineno(1))
            elif tipo_esperado != tipo_retornado and tipo_retornado != 'desconocido':
                mensaje = f"Tipo de retorno inconsistente en la función '{funcion_actual}'. Se esperaba '{tipo_esperado}' pero se retornó '{tipo_retornado}'."
                registrar_error_semantico(mensaje, p.lineno(1))

    p[0] = ('return', p[2])


# --- REGLA PARA BREAK  ---
# AÑADE ESTA NUEVA FUNCIÓN
def p_instruccion_break(p):
    'instruccion_break : BREAK'

    if semantic_context['dentro_de_bucle'] == 0:
        registrar_error_semantico("La instrucción 'break' solo puede usarse dentro de un bucle (for, while).", p.lineno(1))

    p[0] = ('break',)

# --- REGLAS PARA BUCLES (CON SEMÁNTICA PARA 'BREAK') ---

def p_while_loop(p):
    'while_loop : WHILE IPAREN expresion DPAREN enter_loop_scope bloque_codigo'
    semantic_context['dentro_de_bucle'] -= 1
    p[0] = ('while', p[3], p[6])

def p_for_loop(p):
    'for_loop : FOR IPAREN asignacion SENTENCIAFIN expresion SENTENCIAFIN asignacion DPAREN enter_loop_scope bloque_codigo'
    semantic_context['dentro_de_bucle'] -= 1
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_enter_loop_scope(p):
    "enter_loop_scope :"
    semantic_context['dentro_de_bucle'] += 1
#lacedeno11 aporte fin

start = 'programa'
def p_impresion(p):
    '''
    impresion : CONSOLE PUNTO WRITELINE IPAREN imprimible DPAREN
    '''
    p[0] = ('imprimir', p[5])

def p_imprimible(p): 
    '''
    imprimible : expresion
    '''
    p[0] = p[1]
def p_programa(p):
    'programa : lista_sentencias'
    p[0] = p[1]

def p_lista_sentencias(p):
    '''
    lista_sentencias : lista_sentencias sentencia
                     | empty
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [] 
        
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token tipo '{p.type}' con valor '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis inesperado al final del archivo (EOF).")
#lacedeno11 aporte inicio

# --- REGLA PARA SENTENCIAS INDIVIDUALES ---
# Una sentencia puede ser una de varias cosas. Esto hace la gramática modular.
def p_sentencia(p):
    '''
    sentencia : definicion_funcion
              | asignacion SENTENCIAFIN
              | impresion SENTENCIAFIN
              | if_statement
              | while_loop
              | for_loop
              | instruccion_break SENTENCIAFIN   
              | instruccion_return SENTENCIAFIN
    '''
    p[0] = p[1]

def p_definicion_funcion(p):
    'definicion_funcion : tipo_retorno IDENTIFICADOR IPAREN DPAREN enter_function_scope bloque_codigo'
    # Esta regla ahora es más simple. Su único trabajo semántico es limpiar el contexto
    # después de que toda la función ha sido analizada.
    semantic_context['funcion_actual'] = None 
    p[0] = ('def_funcion', p[1], p[2], p[6]) # p[6] es el bloque_codigo

def p_enter_function_scope(p):
    "enter_function_scope :"
    # Esta regla "invisible" se ejecuta ANTES de analizar el bloque de la función.
    # Nos permite establecer el contexto en el momento correcto.
    # Accedemos a los tokens anteriores (nombre y tipo) usando índices negativos.
    nombre_func = p[-3]
    tipo_retorno = p[-4]

    # Registra la función en la tabla de símbolos
    if nombre_func in symbol_table:
        registrar_error_semantico(f"La función '{nombre_func}' ya ha sido definida.", p.lineno(-3))
    else:
        symbol_table[nombre_func] = {'type': 'function', 'return_type': tipo_retorno}

    # Establece el contexto actual, que será usado por 'p_instruccion_return'
    semantic_context['funcion_actual'] = nombre_func
def p_bloque_codigo(p):
    'bloque_codigo : ILLAVE lista_sentencias DLLAVE'
    p[0] = ('bloque', p[2]) # El valor del bloque es la lista de sentencias que contiene

# --- REGLAS PARA IF ---
def p_if_statement(p):
    'if_statement : IF IPAREN expresion DPAREN bloque_codigo'
    p[0] = ('if', p[3], p[5])
# --- REGLAS PARA ASIGNACIÓN ---
def p_asignacion(p):
    '''
    asignacion : tipo_retorno IDENTIFICADOR ASIGNAR expresion
               | IDENTIFICADOR ASIGNAR expresion
    '''
    if len(p) == 5:
        tipo = p[1]
        nombre = p[2]
        valor = p[4]

        tipo_valor = get_expression_type(valor)
        if tipo != tipo_valor and tipo_valor != 'desconocido':
            registrar_error_semantico(f"Tipo incompatible: se esperaba '{tipo}' pero se asignó '{tipo_valor}'.", p.lineno(3))

        if nombre in symbol_table:
            registrar_error_semantico(f"La variable '{nombre}' ya fue declarada.", p.lineno(2))
        else:
            symbol_table[nombre] = {'type': tipo}

        p[0] = ('declaracion_asignacion', tipo, nombre, valor)
    else:
        nombre = p[1]
        valor = p[3]

        if nombre not in symbol_table:
            registrar_error_semantico(f"La variable '{nombre}' no ha sido declarada1.", p.lineno(1))
        else:
            tipo_esperado = symbol_table[nombre]['type']
            tipo_valor = get_expression_type(valor)

            if tipo_esperado != tipo_valor and tipo_valor != 'desconocido':
                registrar_error_semantico(f"Tipo incompatible: la variable '{nombre}' es de tipo '{tipo_esperado}' pero se asignó '{tipo_valor}'.", p.lineno(2))

        p[0] = ('reasignacion', nombre, valor)
        
def p_tipo_retorno(p):
    '''tipo_retorno : INT
                    | FLOAT
                    | STRING
                    | BOOL
                    | VOID'''
    p[0] = p[1]

# --- REGLAS PARA EXPRESIONES (VERSIÓN UNIFICADA) ---

def p_expresion_operadores(p):
    '''
    expresion : expresion MAS expresion
              | expresion MENOS expresion
              | expresion POR expresion
              | expresion DIVIDIR expresion
              | expresion MODULO expresion
              | expresion AND expresion
              | expresion OR expresion
              | expresion MAYOR expresion
              | expresion MENOR expresion
              | expresion MAYORIGUAL expresion
              | expresion MENORIGUAL expresion
              | expresion IGUAL expresion
              | expresion DIFERENTE expresion
    '''
    p[0] = (p[2], p[1], p[3]) # ('+', expr1, expr2)

def p_expresion_unaria(p):
    '''
    expresion : NOT expresion
              | MENOS expresion %prec UMINUS
    '''
    if p[1] == '!':
        p[0] = ('NOT', p[2])
    else:
        p[0] = ('NEG', p[2])

def p_expresion_agrupacion(p):
    'expresion : IPAREN expresion DPAREN'
    p[0] = p[2]

def p_expresion_base(p):
    '''
    expresion : IDENTIFICADOR
              | INT_LITERAL
              | FLOAT_LITERAL
              | STRING_LITERAL
              | TRUE
              | FALSE
    '''
    # Se convierte el valor del token al tipo de dato correcto de Python
    if p.slice[1].type == 'INT_LITERAL':
        p[0] = int(p[1])
    elif p.slice[1].type == 'FLOAT_LITERAL':
        # El lexer captura la 'f' al final, la quitamos para convertir a float
        p[0] = float(p[1][:-1])
    else:
        # Los demás tokens (strings, identificadores, booleanos) se mantienen como texto
        p[0] = p[1]

# --- REGLA PARA ELEMENTOS OPCIONALES (VACÍOS) ---
# Necesaria para listas de sentencias vacías en un bloque de código.
def p_empty(p):
    'empty :'
    pass

#lacedeno11 aporte fin
from my_app.logic.lexico import lexer
parser = yacc.yacc()
def syntaxGUI(input):
    output=[]
    while input is not '':
        result = parser.parse(input)
        output.append(result + "\n")
        
    return output
# --- MODO INTERACTIVO ---
def main():
    username_input = input("Quien esta probando el analizador? \n 1.lolothens-e \n 2.ArielV17 \n 3.lacedeno11\n> ")
    while username_input not in ["1", "2", "3"]:
        print("Seleccione un usuario válido:")    
        username_input = input("Quien esta probando el analizador? \n 1.lolothens-e \n 2.ArielV17 \n 3.lacedeno11\n> ")

    usernames = {
        "1": "lolothens-e",
        "2": "ArielV17",
        "3": "lacedeno11"
    }
    username = usernames[username_input]

    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%Hh%M")
    log_filename = f"semantico-{username}-{timestamp}.txt"
    log_path = "logs/" + log_filename
    chat_log = []

    print("\nEscribe 'exit' para terminar la sesión.\nPuedes escribir bloques multilínea, termina con llaves balanceadas.\n")
    while True:
        user_lines = []
        open_braces = 0
        close_braces = 0
        while True:
            prompt = "C# > " if not user_lines else "... "
            user_input = input(prompt)
            if not user_lines and user_input.strip().lower() == "exit":
                chat_log.append("C# > exit")
                break
            user_lines.append(user_input)
            open_braces += user_input.count('{')
            close_braces += user_input.count('}')
            if open_braces > 0 and open_braces == close_braces:
                break
            if open_braces == 0:
                break
        if not user_lines:
            break
        code_block = '\n'.join(user_lines)
        chat_log.append(f"C# > {code_block}")
        try:
            result = parser.parse(code_block, lexer=lexer)
            if errores_semanticos:
                for err in errores_semanticos:
                    print(err)
                    chat_log.append(err)
                errores_semanticos.clear()
            else:
                print(result)
                chat_log.append(str(result))
        except Exception as e:
            error_msg = f"[Error] {e}"
            print(error_msg)
            chat_log.append(error_msg)
        if user_lines and user_lines[0].strip().lower() == "exit":
            break
    # Guardar el chat en logs
    with open(log_path, "w", encoding='utf-8') as file:
        for line in chat_log:
            file.write(line + "\n")
    print(f"\nSesión guardada en {log_path}")

if __name__ == "__main__":
    main()

#ArielV17 inicio

def p_asignacion_compleja(p):
    '''
    asignacion : tipo_retorno IDENTIFICADOR ASIGNAR expresion
               | tipo_lista IDENTIFICADOR ASIGNAR expresion_lista
               | tipo_array IDENTIFICADOR ASIGNAR expresion_array
    '''
    tipo = p[1]
    nombre = p[2]
    valor = p[4]

    if nombre in symbol_table:
        registrar_error_semantico(f"La variable '{nombre}' ya fue declarada.", p.lineno(2))
    else:
        if isinstance(valor, tuple) and valor[0] == 'nueva_lista':
            tipo_valor = f"List<{valor[1].split('<')[1].rstrip('>')}>"
        elif isinstance(valor, tuple) and valor[0] == 'nuevo_array':
            tipo_valor = valor[1].split()[1] + '[]'
        else:
            tipo_valor = get_expression_type(valor)

        if tipo != tipo_valor and tipo_valor != 'desconocido':
            registrar_error_semantico(
                f"Tipo incompatible: se esperaba '{tipo}' pero se asignó '{tipo_valor}'.",
                p.lineno(3)
            )

        symbol_table[nombre] = {'type': tipo}

    p[0] = ('asignacion_compleja', tipo, nombre, valor)

# --- Tipos compuestos ---
def p_tipo_lista(p):
    '''
    tipo_lista : LISTA
    '''
    tipo_raw = p[1]
    tipo_solo = tipo_raw.split()[0]  # De "List<int> numeros" => "List<int>"
    p[0] = tipo_solo

def p_tipo_array(p):
    '''
    tipo_array : ARRAY_DECLARATION
    '''
    p[0] = p[1]

# --- Expresiones para listas ---
def p_expresion_lista(p):
    '''
    expresion_lista : NEW LISTA IPAREN DPAREN
    '''
    p[0] = ('nueva_lista', p[2])

# --- Expresiones para arrays ---
def p_expresion_array(p):
    '''
    expresion_array : ARRAY_CREATION
    '''
    p[0] = ('nuevo_array', p[1])

# --- Expresiones condicionales combinadas ---
def p_expresion_condicional(p):
    '''
    expresion : expresion AND expresion
              | expresion OR expresion
              | expresion MAYOR expresion
              | expresion MENOR expresion
              | expresion IGUAL expresion
              | expresion DIFERENTE expresion
              | expresion MAYORIGUAL expresion
              | expresion MENORIGUAL expresion
    '''
    p[0] = (p[2], p[1], p[3])

tipos_primitivos = ['int', 'float', 'double', 'bool', 'string', 'char']

def tipo_expresion(expr):
    if isinstance(expr, str):
        if expr.isdigit():
            return 'int'
        if expr.replace('.', '', 1).isdigit():
            return 'float'
        if expr.startswith('"') and expr.endswith('"'):
            return 'string'
        if expr.startswith("'") and expr.endswith("'"):
            return 'char'
        if expr in ['true', 'false']:
            return 'bool'
        return 'variable'

    if isinstance(expr, tuple):
        operador = expr[0]

        if operador in ['+', '-', '*', '/']:
            tipo1 = tipo_expresion(expr[1])
            tipo2 = tipo_expresion(expr[2])

            if tipo1 == 'bool' or tipo2 == 'bool':
                raise Exception(f"Error: No se pueden usar booleanos en operaciones aritméticas ({tipo1} {operador} {tipo2})")

            if tipo1 == tipo2:
                return tipo1
            elif 'float' in [tipo1, tipo2] or 'double' in [tipo1, tipo2]:
                return 'float'
            else:
                raise Exception(f"Tipos incompatibles en operación aritmética: {tipo1} {operador} {tipo2}")

def verificar_asignacion(nodo):
    if nodo[0] == 'declaracion_asignacion':
        tipo_destino = nodo[1]
        valor = nodo[3]

        tipo_valor = tipo_expresion(valor)

        if tipo_destino == tipo_valor:
            return  # Ok

        # Verifica casos especiales
        if tipo_destino == 'int' and tipo_valor == 'float':
            raise Exception(f"Error: No se puede asignar un float a un int sin casting explícito")

        if tipo_destino == 'float' and tipo_valor == 'int':
            return  # Permitido implícitamente

        raise Exception(f"Error: Asignación incompatible de {tipo_valor} a {tipo_destino}")

#ArielV17 fin
