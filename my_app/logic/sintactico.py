import ply.yacc as yacc
from logic.lexico import tokens, lexer

# --- ESTRUCTURAS GLOBALES ---
symbol_table = {}
errores_semanticos = []
semantic_context = {
    'dentro_de_bucle': 0,
    'funcion_actual': None,
}

# --- PRECEDENCIA DE OPERADORES ---
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'IGUAL', 'DIFERENTE'),
    ('nonassoc', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIR', 'MODULO'),
    ('right', 'NOT'),
    ('right', 'UMINUS'),
)

# --- FUNCIÓN PARA REGISTRAR ERRORES ---
def registrar_error_semantico(mensaje, linea):
    """Función centralizada para registrar errores semánticos."""
    error = f"[Error Semántico] Línea {linea}: {mensaje}"
    if error not in errores_semanticos:
        errores_semanticos.append(error)

# --- FUNCIÓN PARA OBTENER TIPOS DE EXPRESIONES ---
import re

def get_expression_type(node, lineno):
    if node is None: return 'desconocido'
    if isinstance(node, int): return 'int'
    if isinstance(node, float): return 'float'
    if isinstance(node, str):
        if node in ('true', 'false'): return 'bool'
        if node.startswith('"') and node.endswith('"'): return 'string'
        if node.startswith("'") and node.endswith("'"): return 'char'
        if node in symbol_table:
            return symbol_table[node].get('type', 'desconocido')
        else:
            registrar_error_semantico(f"La variable '{node}' no ha sido declarada.", lineno)
            return 'desconocido'

    if isinstance(node, tuple):
        op = node[0]
        if op == 'nuevo_diccionario' or op == 'nueva_lista':
            return node[1]
        if op == 'nuevo_array':
            # node[1] es el string de creación, ej: 'new string[5]'
            match = re.match(r'new\s+(int|float|bool|string|char)', node[1])
            if match:
                base_type = match.group(1)
                return f"array-{base_type}"
            return 'desconocido_array_creacion'
        if op == 'array_llaves':
            if node[1]:
                first_element_type = get_expression_type(node[1][0], lineno)
                return f"array-{first_element_type}"
            return 'array-empty'
        if op in ('+', '-', '*', '/', '%'):
            tipo1 = get_expression_type(node[1], lineno)
            tipo2 = get_expression_type(node[2], lineno)
            tipos_numericos = ('int', 'float')
            if tipo1 not in tipos_numericos or tipo2 not in tipos_numericos:
                registrar_error_semantico(f"Operación aritmética inválida entre los tipos '{tipo1}' y '{tipo2}'.", lineno)
                return 'desconocido'
            if 'float' in (tipo1, tipo2):
                return 'float'
            else:
                return 'int'
        if op in ('<', '>', '<=', '>=', '==', '!=', '&&', '||', '!', 'NOT'):
            return 'bool'
    return 'desconocido'

# --- INICIO DE LA GRAMÁTICA (YACC) ---

start = 'programa'

def p_programa(p):
    '''
    programa : lista_sentencias
    '''
    p[0] = p[1]

def p_lista_sentencias(p):
    '''
    lista_sentencias : lista_sentencias sentencia
                     | empty
    '''
    if len(p) == 3:
        if p[1] is None: p[1] = []
        if p[2] is not None: p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = []

# --- CORRECCIÓN 2: Unificar todas las sentencias en una sola regla ---
def p_sentencia(p):
    '''
    sentencia : declaracion SENTENCIAFIN
              | asignacion_elemento SENTENCIAFIN
              | if_statement
              | while_loop
              | for_loop
              | impresion SENTENCIAFIN
              | instruccion_return SENTENCIAFIN
              | instruccion_break SENTENCIAFIN
    '''
    p[0] = p[1]

# --- REGLAS DE DECLARACIÓN Y ASIGNACIÓN ---

def p_declaracion(p):
    '''
    declaracion : tipo_dato IDENTIFICADOR ASIGNAR expresion
                | tipo_array IDENTIFICADOR ASIGNAR expresion_array
                | IDENTIFICADOR ASIGNAR expresion
    '''
    if len(p) == 5:
        tipo_declarado = p[1]
        nombre = p[2]
        valor = p[4]

        if nombre in symbol_table:
            registrar_error_semantico(f"La variable '{nombre}' ya fue declarada.", p.lineno(2))
        else:
            tipo_valor_real = get_expression_type(valor, p.lineno(3))
            # Manejo especial para arrays
            if isinstance(tipo_declarado, str) and tipo_declarado.endswith('[]') and tipo_valor_real.startswith('array-'):
                base_tipo_declarado = tipo_declarado.replace('[]', '').strip()
                base_tipo_valor_real = tipo_valor_real.split('-')[-1].strip()
                if base_tipo_declarado != base_tipo_valor_real:
                    registrar_error_semantico(f"Tipo incompatible para array. Se esperaba array de '{base_tipo_declarado}' pero se asignó array de '{base_tipo_valor_real}'.", p.lineno(3))
                symbol_table[nombre] = {'type': tipo_declarado}
            elif tipo_declarado != tipo_valor_real and tipo_valor_real != 'desconocido':
                registrar_error_semantico(f"Tipo incompatible. No se puede asignar '{tipo_valor_real}' a una variable de tipo '{tipo_declarado}'.", p.lineno(3))
            else:
                symbol_table[nombre] = {'type': tipo_declarado}
        p[0] = ('declaracion', tipo_declarado, nombre, valor)
    # Caso: x = 10;
    else:
        nombre = p[1]
        valor = p[3]
        if nombre not in symbol_table:
            registrar_error_semantico(f"La variable '{nombre}' no ha sido declarada.", p.lineno(1))
        else:
            tipo_esperado = symbol_table[nombre]['type']
            tipo_valor_real = get_expression_type(valor, p.lineno(2))
            if tipo_esperado != tipo_valor_real and tipo_valor_real != 'desconocido':
                registrar_error_semantico(f"Tipo incompatible. No se puede asignar '{tipo_valor_real}' a la variable '{nombre}' de tipo '{tipo_esperado}'.", p.lineno(2))
        p[0] = ('reasignacion', nombre, valor)

# --- CORRECCIÓN 3: Esta es la regla clave para la validación de Dictionary ---
def p_asignacion_elemento(p):
    '''
    asignacion_elemento : IDENTIFICADOR ICORCH expresion DCORCH ASIGNAR expresion
    '''
    nombre_dic = p[1]
    clave = p[3]
    valor = p[6]

    if nombre_dic not in symbol_table:
        registrar_error_semantico(f"La colección '{nombre_dic}' no ha sido declarada.", p.lineno(1))
    else:
        tipo_declarado = symbol_table[nombre_dic].get('type')
        if not tipo_declarado or not tipo_declarado.startswith('Dictionary'):
            registrar_error_semantico(f"La variable '{nombre_dic}' no es un diccionario y no puede usar el operador [].", p.lineno(1))
            p[0] = ('error', 'acceso_invalido')
            return

        try:
            tipos_internos = tipo_declarado.replace('Dictionary<', '').replace('>', '').split(',')
            tipo_clave_esperado = tipos_internos[0].strip()
            tipo_valor_esperado = tipos_internos[1].strip()

            tipo_clave_real = get_expression_type(clave, p.lineno(2))
            tipo_valor_real = get_expression_type(valor, p.lineno(5))

            if tipo_clave_esperado != tipo_clave_real and tipo_clave_real != 'desconocido':
                registrar_error_semantico(f"Error de tipo en la clave. Se esperaba '{tipo_clave_esperado}' pero se usó '{tipo_clave_real}'.", p.lineno(2))
            
            if tipo_valor_esperado != tipo_valor_real and tipo_valor_real != 'desconocido':
                registrar_error_semantico(f"Error de tipo en el valor. Se esperaba '{tipo_valor_esperado}' pero se asignó '{tipo_valor_real}'.", p.lineno(5))
        except (IndexError, AttributeError):
            registrar_error_semantico(f"Error al procesar el tipo del diccionario '{nombre_dic}'.", p.lineno(1))

    p[0] = ('asignacion_elemento', nombre_dic, clave, valor)

# --- REGLAS PARA DEFINIR TIPOS DE DATOS ---
def p_tipo_dato(p):
    '''
    tipo_dato : tipo_retorno
              | tipo_lista
              | tipo_diccionario
    '''
    p[0] = p[1]

def p_tipo_retorno(p):
    '''
    tipo_retorno : INT
                 | FLOAT
                 | STRING
                 | BOOL
                 | VOID
                 | CHAR
    '''
    p[0] = p[1]

def p_tipo_lista(p):
    'tipo_lista : LISTA MENOR tipo_retorno MAYOR'
    p[0] = f"List<{p[3]}>"

def p_tipo_diccionario(p):
    'tipo_diccionario : DICTIONARY MENOR tipo_retorno COMA tipo_retorno MAYOR'
    p[0] = f"Dictionary<{p[3]},{p[5]}>"

# --- REGLA PARA TIPO ARRAY ---
def p_tipo_array(p):
    'tipo_array : ARRAY_TYPE'
    p[0] = p[1]



# --- REGLAS PARA EXPRESIONES (Creación de colecciones, operadores, etc.) ---
def p_expresion(p):
    '''
    expresion : expresion_aritmetica
              | expresion_logica
              | valor_literal
              | IDENTIFICADOR
              | expresion_lista
              | expresion_diccionario
              | expresion_array
    '''
    p[0] = p[1]

def p_expresion_aritmetica(p):
    '''
    expresion_aritmetica : expresion MAS expresion
                         | expresion MENOS expresion
                         | expresion POR expresion
                         | expresion DIVIDIR expresion
                         | MENOS expresion %prec UMINUS
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = ('NEG', p[2])

def p_expresion_logica(p):
    '''
    expresion_logica : expresion MAYOR expresion
                     | expresion MENOR expresion
                     | expresion MAYORIGUAL expresion
                     | expresion MENORIGUAL expresion
                     | expresion IGUAL expresion
                     | expresion DIFERENTE expresion
                     | expresion AND expresion
                     | expresion OR expresion
                     | NOT expresion
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = ('NOT', p[2])

def p_expresion_agrupacion(p):
    'expresion : IPAREN expresion DPAREN'
    p[0] = p[2]

def p_valor_literal(p):
    '''
    valor_literal : INT_LITERAL
                  | FLOAT_LITERAL
                  | STRING_LITERAL
                  | CHAR_LITERAL
                  | TRUE
                  | FALSE
    '''
    p[0] = p[1]

def p_expresion_lista(p):
    'expresion_lista : NEW tipo_lista IPAREN DPAREN'
    p[0] = ('nueva_lista', p[2])

def p_expresion_diccionario(p):
    'expresion_diccionario : NEW tipo_diccionario IPAREN DPAREN'
    p[0] = ('nuevo_diccionario', p[2])

def p_expresion_array(p):
    '''
    expresion_array : ARRAY_CREATION
                    | ILLAVE lista_elementos_array DLLAVE
    '''
    if len(p) == 2:
        p[0] = ('nuevo_array', p[1])
    else:
        p[0] = ('array_llaves', p[2])

def p_lista_elementos_array(p):
    '''
    lista_elementos_array : expresion COMA lista_elementos_array
                        | expresion
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# --- REGLAS PARA ESTRUCTURAS DE CONTROL ---

def p_if_statement(p):
    'if_statement : IF IPAREN expresion DPAREN bloque_codigo'
    p[0] = ('if', p[3], p[5])

def p_while_loop(p):
    'while_loop : WHILE IPAREN expresion DPAREN enter_loop_scope bloque_codigo'
    semantic_context['dentro_de_bucle'] -= 1
    p[0] = ('while', p[3], p[6])

def p_for_loop(p):
    'for_loop : FOR IPAREN declaracion SENTENCIAFIN expresion SENTENCIAFIN expresion DPAREN enter_loop_scope bloque_codigo'
    semantic_context['dentro_de_bucle'] -= 1
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_enter_loop_scope(p):
    'enter_loop_scope :'
    semantic_context['dentro_de_bucle'] += 1

def p_bloque_codigo(p):
    'bloque_codigo : ILLAVE lista_sentencias DLLAVE'
    p[0] = p[2]

# --- OTRAS INSTRUCCIONES ---

def p_impresion(p):
    'impresion : CONSOLE PUNTO WRITELINE IPAREN expresion DPAREN'
    p[0] = ('imprimir', p[5])

def p_instruccion_return(p):
    'instruccion_return : RETURN expresion'
    p[0] = ('return', p[2])

def p_instruccion_break(p):
    'instruccion_break : BREAK'
    if semantic_context['dentro_de_bucle'] == 0:
        registrar_error_semantico("La instrucción 'break' solo puede usarse dentro de un bucle.", p.lineno(1))
    p[0] = ('break',)

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        registrar_error_semantico(f"Error de sintaxis en '{p.value}'", p.lineno)
    else:
        registrar_error_semantico("Error de sintaxis al final del archivo.", 0)

# --- FUNCIÓN PRINCIPAL DE ANÁLISIS ---

parser = yacc.yacc()

def analizar_codigo(codigo_fuente):
    # Limpiar estado anterior
    symbol_table.clear()
    errores_semanticos.clear()
    semantic_context['dentro_de_bucle'] = 0
    semantic_context['funcion_actual'] = None
    lexer.lineno = 1
    
    # Análisis Léxico
    tokens_lexicos = []
    lexer.input(codigo_fuente)
    while True:
        tok = lexer.token()
        if not tok: break
        tokens_lexicos.append(str(tok))
    
    # Análisis Sintáctico y Semántico
    parser.parse(codigo_fuente, lexer=lexer)
    
    return {
        "tokens": tokens_lexicos,
        "errors": errores_semanticos[:]
    }