import ply.lex as lex
import ply.yacc as yacc, datetime
from logic.lexico import tokens, lexer


#lacedeno11 aporte inicio

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

start = 'programa'

# --- ESTRUCTURAS PARA EL ANÁLISIS SEMÁNTICO ---

semantic_context = {
    'dentro_de_bucle': 0,
    'funcion_actual': None,
    'clase_actual': None 
}

errores_semanticos = []


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

def p_instruccion_break(p):
    'instruccion_break : BREAK'

    if semantic_context['dentro_de_bucle'] == 0:
        registrar_error_semantico("La instrucción 'break' solo puede usarse dentro de un bucle (for, while).", p.lineno(1))

    p[0] = ('break',)

def p_while_loop(p):
    'while_loop : WHILE IPAREN expresion DPAREN enter_loop_scope bloque_codigo'
    semantic_context['dentro_de_bucle'] -= 1
    p[0] = ('while', p[3], p[6])

def p_for_operables(p):
    '''
    for_operables : incremento 
                  | decremento
    '''
    p[0] = p[1]
    
def p_for_loop(p):
    'for_loop : FOR IPAREN asignacion expresion SENTENCIAFIN for_operables DPAREN enter_loop_scope bloque_codigo'
    semantic_context['dentro_de_bucle'] -= 1
    p[0] = ('for', p[3], p[5], p[8])
    
    if get_expression_type(p[4]) != 'bool':
        registrar_error_semantico("La condición del 'for' debe ser una expresión booleana.", p.lineno(4))


def p_enter_loop_scope(p):
    "enter_loop_scope :"
    semantic_context['dentro_de_bucle'] += 1
#lacedeno11 aporte fin

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
    
def p_package_route(p):
    '''
    package_route : IDENTIFICADOR PUNTO package_route
                  | IDENTIFICADOR  
    '''
    
def p_imports(p):
    '''
    imports : IMPORT package_route NEWLINE imports
            | IMPORT package_route
    '''
    
def p_programa(p):
    '''
    programa : imports definicion_clase
             | definicion_clase
                '''


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
        print("Error: Se esperaba más código, pero se encontró el final del archivo (EOF).")
#lacedeno11 aporte inicio
def p_incremento(p):
    'incremento : IDENTIFICADOR INCREMENTO'
    p[0] = p[1]+p[2]
    
def p_decremento(p):
    'decremento : IDENTIFICADOR DECREMENTO'
    p[0] = p[1]+p[2]
    
# --- REGLA PARA SENTENCIAS INDIVIDUALES ---
# Una sentencia puede ser una de varias cosas. Esto hace la gramática modular.
def p_sentencia(p):
    '''
    sentencia : definicion_funcion
              | asignacion SENTENCIAFIN
              | impresion SENTENCIAFIN
              | incremento SENTENCIAFIN
              | decremento SENTENCIAFIN
              | if_statement
              | if_else_statement
              | while_loop
              | for_loop
              | instruccion_break SENTENCIAFIN   
              | instruccion_return SENTENCIAFIN
    '''
    p[0] = p[1]
    
def p_modificador_acceso(p):
    '''
    modificador_acceso : PUBLIC
                  | PRIVATE 
                  | PROTECTED
                  | INTERNAL
                  | PROTECTED INTERNAL
                  | PRIVATE PROTECTED
    '''
    
def p_definicion_clase(p):
    '''
    definicion_clase : modificador_acceso tipo_retorno CLASS IDENTIFICADOR ILLAVE enter_class_scope bloque_codigo DLLAVE
    '''

def p_enter_class_scope(p):
    "enter_class_scope :"
    nombre_clas = p[-3]
    tipo_retorno = p[-4]

    # Registra la función en la tabla de símbolos
    if nombre_clas in symbol_table:
        registrar_error_semantico(f"La clase '{nombre_clas}' ya ha sido definida.", p.lineno(-3))
    else:
        symbol_table[nombre_clas] = {'type': 'class', 'return_type': tipo_retorno}

    # Establece el contexto actual, que será usado por 'p_instruccion_return'
    semantic_context['clase_actual'] = nombre_clas



def p_definicion_funcion(p):
    'definicion_funcion : tipo_retorno IDENTIFICADOR IPAREN DPAREN enter_function_scope bloque_codigo'
    semantic_context['funcion_actual'] = None 
    p[0] = ('def_funcion', p[1], p[2], p[6]) # p[6] es el bloque_codigo

def p_enter_function_scope(p):
    "enter_function_scope :"
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

def p_if_statement(p):
    'if_statement : IF IPAREN expresion DPAREN bloque_codigo'
    p[0] = ('if', p[3], p[5])
    
def p_if_else_statement(p):
    'if_else_statement : IF IPAREN expresion DPAREN bloque_codigo ELSE bloque_codigo'
    p[0] = ('if', p[3], p[5], 'else', p[7])
    

def p_asignacion(p):
    '''
    asignacion : tipo_retorno IDENTIFICADOR ASIGNAR expresion SENTENCIAFIN
               | IDENTIFICADOR ASIGNAR expresion SENTENCIAFIN
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
            registrar_error_semantico(f"La variable '{nombre}' no ha sido declarada.", p.lineno(1))
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
    if p.slice[1].type == 'INT_LITERAL':
        p[0] = int(p[1])
    elif p.slice[1].type == 'FLOAT_LITERAL':
        p[0] = float(p[1].rstrip('fF'))
    else:
        p[0] = p[1]


def p_empty(p):
    'empty :'
    pass

#lacedeno11 aporte fin

#ArielV17 inicio

def p_asignacion_compleja(p):
    '''
    asignacion : tipo_lista IDENTIFICADOR ASIGNAR expresion_lista SENTENCIAFIN
               | tipo_array IDENTIFICADOR ASIGNAR expresion_array SENTENCIAFIN
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
    tipo_lista : LISTA MENOR tipo_retorno MAYOR 
    '''
    tipo = p[3]

def p_tipo_array(p):
    '''
    tipo_array : ARRAY_DECLARATION
    '''
    p[0] = p[1]

# --- Expresiones para listas ---
def p_expresion_lista(p):
    '''
    expresion_lista : NEW LISTA MENOR tipo_retorno MAYOR IPAREN DPAREN
                    | NEW LISTA MENOR tipo_retorno MAYOR ILLAVE elementos DLLAVE
    '''
    if len(p) == 8: 
        tipo = p[4]
        p[0] = ('nueva_lista', f"List<{tipo}>", [])
    else:
        tipo_decl = p[4]
        tipo_real, valores = p[7]

        if tipo_decl != tipo_real and tipo_real != 'desconocido':
            registrar_error_semantico(f"Tipo declarado 'List<{tipo_decl}>' no coincide con el tipo de elementos '{tipo_real}'", p.lineno(1))

        p[0] = ('nueva_lista', f"List<{tipo_decl}>", valores)

def p_primitivo(p):
    '''
    primitivo : FLOAT_LITERAL
             | INT_LITERAL
             | CHAR_LITERAL
             | STRING_LITERAL
             | BOOL_LITERAL
    '''
    token_type = p.slice[1].type
    value = p[1]

    if token_type == 'FLOAT_LITERAL':
        p[0] = ('float', float(value.rstrip('fF')))
    elif token_type == 'INT_LITERAL':
        p[0] = ('int', int(value))
    elif token_type == 'CHAR_LITERAL':
        p[0] = ('char', value)
    elif token_type == 'STRING_LITERAL':
        p[0] = ('string', value)
    elif token_type == 'BOOL_LITERAL':
        p[0] = ('bool', value.lower() == 'true')
    
def p_elementos(p):
    '''
    elementos : primitivo COMA elementos 
                | primitivo 
    '''
    if len(p) == 2:
        tipo, valor = p[1]
        p[0] = (tipo, [valor])
    else:
        tipo1, valor1 = p[1]
        tipo2, valores_restantes = p[3]
        
        if tipo1 != tipo2:
            tipo_final=tipo2
        else:
            tipo_final = tipo1

        p[0] = (tipo_final, [valor1] + valores_restantes)


def p_expresion_array(p):
    '''
    expresion_array : ARRAY_CREATION
    '''
    p[0] = ('nuevo_array', p[1])


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

parser = yacc.yacc()

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


def analizar_codigo(codigo_fuente):
    """
    Esta función centraliza el análisis léxico, sintáctico y semántico.
    Es la única función que el servidor Flask necesita llamar.
    """
    symbol_table.clear()
    errores_semanticos.clear()
    semantic_context['dentro_de_bucle'] = 0
    semantic_context['funcion_actual'] = None
    lexer.lineno = 1

    # 2. Análisis Léxico: Obtener la lista de tokens
    tokens_lexicos = []
    try:
        lexer.input(codigo_fuente)
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens_lexicos.append(str(tok))
    except Exception as e:
        errores_semanticos.append(f"[Error Léxico Crítico] {e}")


    # 3. Análisis Sintáctico y Semántico
    # Reiniciar el lexer para el parser
    lexer.input(codigo_fuente) 
    if not errores_semanticos: # Solo intentar parsear si el lexer no falló
        try:
            # El parser de YACC llamará a tus reglas p_...
            # y estas llenarán la lista `errores_semanticos` si algo sale mal.
            parser.parse(codigo_fuente, lexer=lexer)
        except Exception as e:
            # Capturar errores inesperados del propio parser
            errores_semanticos.append(f"[Errores sintácticos detectados] {e}")

    # 4. Devolver un diccionario con todos los resultados
    return {
        "tokens": tokens_lexicos,
        "errors": errores_semanticos[:] # Devolvemos una copia de los errores
    }

