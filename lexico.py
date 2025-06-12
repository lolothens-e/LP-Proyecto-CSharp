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

) + tuple(reserved.values())

#delimitadores
t_SENTENCIAFIN = r';'
t_IPAREN  = r'\('
t_DPAREN  = r'\)'
t_ILLAVE = r'\{'
t_DLLAVE = r'\}'
t_ICORCH = r'\['
t_DCORCH = r'\]'

# Regular expression rules for simple tokens
def t_VARIABLE(t):
    r'[_a-zA-Z][_a-zA-Z0-9]+'
    t.type = reserved.get(t.value,'VARIABLE')
    return t
    

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t' # A string containing ignored characters (spaces and tabs)

lexer = lex.lex()

# Test it out
data = '''
hello 
Lok90Lew 
_name 
asd
asdasd;_aster
count2
int
(()
[[]]
{{{
}
'''

# Give the lexer some input
lexer.input(data)

# Get user selection and map it to usernames
username_input = input("Quien esta probando el analizador? \n 1.lolothens-e \n 2.ArielV17 \n 3.Abrahan\n> ")
while username_input not in ["1", "2", "3"]:
    print("Seleccione usuario valido:")    
    username_input = input("Quien esta probando el analizador? \n 1.lolothens-e \n 2.ArielV17 \n 3.Abrahan\n> ")

# Map input to usernames
usernames = {
    "1": "lolothens-e",
    "2": "ArielV17",
    "3": "Abrahan"
}
username = usernames[username_input]

# Timestamp and filename
now = datetime.datetime.now()
timestamp = now.strftime("%d-%m-%Y_%Hh%M")
filename = f"lexico-{username}-{timestamp}.txt"

# Open file for writing
with open(filename, "w") as file:
    # Token loop
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)                 # print to console
        file.write(str(tok) + "\n")  # write to file
