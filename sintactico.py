import ply.yacc as yacc, datetime
from lexico import tokens

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

# Una lista de sentencias puede ser una sentencia seguida de más sentencias, o estar vacía.
def p_lista_sentencias(p):
    '''
    lista_sentencias : lista_sentencias sentencia
                     | empty
    '''
    # La lógica de construcción de la lista también cambia ligeramente
    if len(p) == 3:
        p[0] = p[1] + [p[2]] # Añade la nueva sentencia al final de la lista existente
    else:
        p[0] = [] # La lista empieza vacía
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
    '''
    p[0] = p[1]

# --- REGLAS PARA FUNCIONES ---
def p_definicion_funcion(p):
    'definicion_funcion : tipo_retorno IDENTIFICADOR IPAREN DPAREN bloque_codigo'
    # Simplificado: sin parámetros. Se pueden añadir más adelante.
    p[0] = ('def_funcion', p[1], p[2], p[5])

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
        p[0] = ('declaracion_asignacion', p[1], p[2], p[4])
    else:
        p[0] = ('reasignacion', p[1], p[3])
        
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
    p[0] = p[1]

# --- REGLA PARA ELEMENTOS OPCIONALES (VACÍOS) ---
# Necesaria para listas de sentencias vacías en un bloque de código.
def p_empty(p):
    'empty :'
    pass

#lacedeno11 aporte fin
from lexico import lexer

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

ruta_archivo = input('Escribe la ruta del archivo a analizar y presiona Enter: ')

parser = yacc.yacc()

try:
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        data = file.read()
        print(f"\n--- Analizando el archivo: {ruta_archivo} ---")
        
        result = parser.parse(data, lexer=lexer)
        
        print("\n--- Resultado del Análisis Sintáctico (AST) ---")
        print(result)
        
        now = datetime.datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%Hh%M")
        log_filename = f"sintactico-{username}-{timestamp}.txt"

        import os
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        with open("logs/" + log_filename, "w", encoding='utf-8') as log_file:
            if result:
                log_file.write(str(result))
            else:
                log_file.write("El análisis no produjo resultados (posiblemente por errores de sintaxis).")

        print(f"\nAnálisis completado. Resultado guardado en 'logs/{log_filename}'")

except FileNotFoundError:
    print(f"\nError Crítico: No se pudo encontrar el archivo en la ruta '{ruta_archivo}'.")
    print("Por favor, verifica que la ruta sea correcta y vuelve a intentarlo.")
except Exception as e:
    print(f"\nOcurrió un error inesperado durante el análisis: {e}")

#ArielV17 inicio

# --- Asignación con tipos primitivos, listas y arrays ---
def p_asignacion_compleja(p):
    '''
    asignacion : tipo_retorno IDENTIFICADOR ASIGNAR expresion
               | tipo_lista IDENTIFICADOR ASIGNAR expresion_lista
               | tipo_array IDENTIFICADOR ASIGNAR expresion_array
    '''
    p[0] = ('asignacion_compleja', p[1], p[2], p[4])

# --- Tipos compuestos ---
def p_tipo_lista(p):
    '''
    tipo_lista : LISTA
    '''
    p[0] = p[1]

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

#ArielV17 fin
