import ply.lex as lex,  datetime

reserved = {
    'import': 'IMPORT',
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
    'operator': 'OPERATOR',
    'Dictionary': 'DICTIONARY',#lacedeno11
    'List': 'LISTA',
    'Console' : 'CONSOLE',
    'WriteLine' : 'WRITELINE'
}


tokens = (
    'IDENTIFICADOR',
    'SENTENCIAFIN',
    'IPAREN',
    'DPAREN',
    'ILLAVE',
    'DLLAVE',
    'ICORCH',
    'DCORCH',
    'ID_INVALIDO',
    'GENERICO_INVALIDO',
    'INT_LITERAL', #Tokens Ariel
    'FLOAT_LITERAL',
    'CHAR_LITERAL',
    'STRING_LITERAL',
    'BOOL_LITERAL',
    'ARRAY_TYPE',
    'ARRAY_CREATION', #Fin tokens Ariel
    #lacedeno11  inicio
    # Operadores Aritméticos
    'MAS', 'MENOS', 'POR', 'DIVIDIR', 'MODULO', 'INCREMENTO', 'DECREMENTO',
    # Operadores de Asignación
    'ASIGNAR', 'MASIGUAL', 'MENOSIGUAL', 'PORIGUAL', 'DIVIDIRIGUAL',
    # Operadores de Comparación
    'IGUAL', 'DIFERENTE', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL',
    # Operadores Lógicos
    'AND', 'OR', 'NOT',
    # Operador Lambda
    'FLECHALAMBDA',
    # Otros símbolos
    'PUNTO', 'COMA', 'NEWLINE', 'ARROBA','FORMAT'
    #lacedeno11  fin

) + tuple(reserved.values())

#Anthony Navarrete inicio
t_SENTENCIAFIN = r';'

t_IPAREN  = r'\('
t_DPAREN  = r'\)'
t_ILLAVE = r'\{'
t_DLLAVE = r'\}'
t_ICORCH = r'\['
t_DCORCH = r'\]'
t_ARROBA = r'@'
t_FORMAT = r'\$'

def t_ARRAY_TYPE(t):
    r'\b(?:int|float|bool|string|char)\s*\[\s*\]'
    return t

    
def t_ID_INVALIDO(t):
    r'[0-9]+[a-zA-Z_][a-zA-Z0-9_]*'
    print(f"Invalid var usage: '{t.value}'")
    t.lexer.skip(len(t.value))
    
def t_IDENTIFICADOR(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'IDENTIFICADOR')
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Anthony Navarrete fin
#lacedeno11 inicio

# Operadores de Asignación y Comparación
t_MASIGUAL     = r'\+='
t_MENOSIGUAL   = r'-='
t_PORIGUAL     = r'\*='
t_DIVIDIRIGUAL = r'/='
t_IGUAL        = r'=='
t_DIFERENTE    = r'!='
t_MAYORIGUAL   = r'>='
t_MENORIGUAL   = r'<='
# Operadores Lógicos, de Incremento/Decremento y Lambda
t_AND          = r'&&'
t_OR           = r'\|\|'
t_INCREMENTO   = r'\+\+'
t_DECREMENTO   = r'--'
t_FLECHALAMBDA = r'=>'
# Operadores y símbolos de un solo caracter
t_ASIGNAR      = r'='
t_MAS          = r'\+'
t_MENOS        = r'-'
t_POR          = r'\*'
t_DIVIDIR      = r'/'
t_MODULO       = r'%'
t_MAYOR        = r'>'
t_MENOR        = r'<'
t_NOT          = r'!'
t_PUNTO        = r'\.'
t_COMA         = r','
#lacedeno11 fin

#INICIO CORRECCIÓN 1: MANEJO DE COMENTARIOS

# Regla para comentarios de múltiples líneas /* ... */
def t_COMMENT_MULTI(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass # No retorna nada, efectivamente ignorando el token

# Regla para comentarios de una sola línea // ...
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass # No retorna nada, ignorando el token


#FIN CORRECCIÓN 1

#Inicio Ariel Villacrés
def t_FLOAT_LITERAL(t):
    r'\d+\.\d+f?'
    t.value = float(t.value.replace('f', '')) 
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR_LITERAL(t):
    r"'\w'"
    return t

def t_STRING_LITERAL(t):
    r'"([^\\"]|\\.)*"'
    return t

def t_BOOL_LITERAL(t):
    r'\btrue\b|\bfalse\b'
    t.type = reserved.get(t.value, 'BOOL_LITERAL')
    return t



def t_ARRAY_CREATION(t):
    r'new\s+(?:int|float|bool|string|char)\s*\[\s*\d+\s*\]'
    return t

#Fin Ariel Villacrés

t_ignore  = ' \t' 

lexer = lex.lex()

# Test it out
data = '''
using System;
using System.Text.RegularExpressions;

class RegexTokenizerTest
{
    static void Main()
    {
        string input = "int value = 42; // This is a comment";
        string pattern = "\w+|[=;]|\S"; // Match words, operators, symbols

        MatchCollection matches = Regex.Matches(input, pattern);

        Console.WriteLine("Tokens:");
        foreach (Match match in matches)
        {
            Console.WriteLine($"[{match.Value}]");
        }
    }
}

'''
# Tabla de símbolos global
symbol_table = {}

def lexicoGUI(input):
    lexer.input(input)
    output = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        output.append(tok + "\n")
    return output

def lexico():
    # Preguntar usuario
    username_input = input("Quien esta probando el analizador? \n 1.lolothens-e \n 2.ArielV17 \n 3.lacedeno11\n> ")
    while username_input not in ["1", "2", "3"]:
        print("Seleccione usuario valido:")    
        username_input = input("Quien esta probando el analizador? \n 1.lolothens-e \n 2.ArielV17 \n 3.lacedeno11\n> ")

    usernames = {
        "1": "lolothens-e",
        "2": "ArielV17",
        "3": "lacedeno11"
    }
    username = usernames[username_input]

    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%Hh%M")
    filename = f"semantico-{username}-{timestamp}.txt"
    log_path = "logs/" + filename
    chat_log = []

    print("\nEscribe 'exit' para terminar la sesión.\n")
    while True:
        user_input = input("C# > ")
        chat_log.append(f"C# > {user_input}")
        if user_input.strip().lower() == "exit":
            break
        # Procesar la línea con el lexer
        lexer.input(user_input)
        output = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            # Ejemplo: añadir identificadores a la tabla de símbolos
            if tok.type == 'IDENTIFICADOR':
                symbol_table[tok.value] = {'type': 'variable', 'lineno': tok.lineno}
            output.append(str(tok))
        if output:
            for line in output:
                print(line)
            chat_log.extend(output)
        else:
            print("(Sin tokens reconocidos)")
            chat_log.append("(Sin tokens reconocidos)")
    # Guardar el chat en logs
    with open(log_path, "w") as file:
        for line in chat_log:
            file.write(line + "\n")
    print(f"\nSesión guardada en {log_path}")

if __name__ == "__main__":
    lexico()