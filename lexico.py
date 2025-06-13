import ply.lex as lex,  datetime, os


reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'do': 'DO',
    'while': 'WHILE',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'goto': 'GOTO',
    'default': 'DEFAULT',
    'yield': 'YIELD',
    'int': 'INT',
    'float': 'FLOAT',
    'double': 'DOUBLE',
    'decimal': 'DECIMAL',
    'bool': 'BOOL',
    'string': 'STRING',
    'char': 'CHAR',
    'byte': 'BYTE',
    'long': 'LONG',
    'short': 'SHORT',
    'sbyte': 'SBYTE',
    'uint': 'UINT',
    'ulong': 'ULONG',
    'ushort': 'USHORT',
    'object': 'OBJECT',
    'void': 'VOID',
    'null': 'NULL',
    'true': 'TRUE',
    'false': 'FALSE',
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'internal': 'INTERNAL',
    'static': 'STATIC',
    'readonly': 'READONLY',
    'const': 'CONST',
    'volatile': 'VOLATILE',
    'sealed': 'SEALED',
    'abstract': 'ABSTRACT',
    'virtual': 'VIRTUAL',
    'override': 'OVERRIDE',
    'partial': 'PARTIAL',
    'new': 'NEW',
    'class': 'CLASS',
    'struct': 'STRUCT',
    'interface': 'INTERFACE',
    'enum': 'ENUM',
    'delegate': 'DELEGATE',
    'event': 'EVENT',
    'namespace': 'NAMESPACE',
    'using': 'USING',
    'this': 'THIS',
    'base': 'BASE',
    'typeof': 'TYPEOF',
    'sizeof': 'SIZEOF',
    'is': 'IS',
    'as': 'AS',
    'in': 'IN',
    'out': 'OUT',
    'ref': 'REF',
    'params': 'PARAMS',
    'stackalloc': 'STACKALLOC',
    'checked': 'CHECKED',
    'unchecked': 'UNCHECKED',
    'try': 'TRY',
    'catch': 'CATCH',
    'finally': 'FINALLY',
    'throw': 'THROW',
    'var': 'VAR',
    'dynamic': 'DYNAMIC',
    'get': 'GET',
    'set': 'SET',
    'add': 'ADD',
    'remove': 'REMOVE',
    'lock': 'LOCK',
    'unsafe': 'UNSAFE',
    'fixed': 'FIXED',
    'extern': 'EXTERN',
    'operator': 'OPERATOR'
}


# List of token names.   This is always required
tokens = (
    'VARIABLE',
    'SENTENCIAFIN',
    'IPAREN',
    'DPAREN',
    'ILLAVE',
    'DLLAVE',
    'ICORCH',
    'DCORCH',
    'LISTA',
    'VAR_INVALIDO',
    'GENERICO_INVALIDO',

) + tuple(reserved.values())

#Anthony Navarrete inicio
t_SENTENCIAFIN = r';'
t_IPAREN  = r'\('
t_DPAREN  = r'\)'
t_ILLAVE = r'\{'
t_DLLAVE = r'\}'
t_ICORCH = r'\['
t_DCORCH = r'\]'


def t_LISTA(t):
    r'List<[a-zA-Z]+>\s[_a-zA-Z][_a-zA-Z0-9]*'
    return t
    
def t_GENERICO_INVALIDO(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*\s*<[^>]*>'
    print(f"Invalid generic type usage: '{t.value}'")
    t.lexer.skip(len(t.value))
    
def t_VAR_INVALIDO(t):
    r'[0-9]+[a-zA-Z_][a-zA-Z0-9_]*'
    print(f"Invalid var usage: '{t.value}'")
    t.lexer.skip(len(t.value))
    
def t_VARIABLE(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'VARIABLE')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Anthony Navarrete fin

t_ignore  = ' \t' # A string containing ignored characters (spaces and tabs)

lexer = lex.lex()

# Test it out
data = '''
using System;
using System.Text.RegularExpressions;
'''

opcion  = input('Escribe la ruta del archivo a analizar o presiona Enter para usar la data cargada en codigo: ')
if opcion.strip() != '':
    try:
        with open(opcion, 'r', encoding='utf-8') as file:
            data = file.read()
    except FileNotFoundError:
        print('No encontramos tu archivo. Usaremos los datos usados en variable data.')


lexer.input(data)

username_input = input("Quien esta probando el analizador? \n 1.lolothens-e \n 2.ArielV17 \n 3.Abrahan\n> ")
while username_input not in ["1", "2", "3"]:
    print("Seleccione usuario valido:")    
    username_input = input("Quien esta probando el analizador? \n 1.lolothens-e \n 2.ArielV17 \n 3.Abrahan\n> ")

usernames = {
    "1": "lolothens-e",
    "2": "ArielV17",
    "3": "Abrahan"
}
username = usernames[username_input]

now = datetime.datetime.now()
timestamp = now.strftime("%d-%m-%Y_%Hh%M")
filename = f"lexico-{username}-{timestamp}.txt"

with open("logs/"+filename, "w") as file:
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)                 
        file.write(str(tok) + "\n")  
