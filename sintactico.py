import ply.yacc as yacc
from lexico import tokens

def p_clase(p):
    ''' 
    CLASS VARIABLE ILLAVE cuerpo DLLAVE
    '''
    
def p_metodo(p):
    ''' 
    CLASS VARIABLE ILLAVE cuerpo DLLAVE
    '''


def p_cuerpo(p):
    '''cuerpo : linea 
            | linea cuerpo
    '''
def p_linea(p):
    '''linea : expression SENTENCIAFIN
        | assignment SENTENCIAFIN '''

def p_expression_plus(p):
    'expression : expression MAS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MENOS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term POR factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDIR factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    '''factor : INT_LITERAL
                | FLOAT_LITERAL
    '''
    p[0] = p[1]

def p_factor_expr(p):
    'factor : IPAREN expression DPAREN'
    p[0] = p[2]

def p_valor(p):
    '''
    valor : LISTA 
            | INT_LITERAL 
            | FLOAT_LITERAL 
            | CHAR_LITERAL
            | STRING_LITERAL 
            | BOOL_LITERAL 
    '''

def p_assignment(p):
    '''
    assignment : VARIABLE ASIGNAR valor
    '''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('C# > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)