import ply.yacc as yacc, datetime
from lexico import tokens

p_start= 'cuerpo'

def p_impresion(p):
    '''
    impresion : CONSOLE PUNTO WRITELINE IPAREN imprimibles DPAREN SENTENCIAFIN
    '''
def p_imprimibles(p):
    '''
        imprimibles : IDENTIFICADOR
        | BOOL_LITERAL
        | CHAR_LITERAL
        | STRING_LITERAL
        | FLOAT_LITERAL
        | INT_LITERAL
    '''

def p_linea(p): #AGREGAR CONFORMA AVANZA
    '''
    linea : impresion 
    '''
 
def p_cuerpo(p): 
    '''
    cuerpo : linea
    | linea cuerpo
    '''
       

def p_error(p):
    print("Syntax error in input!")

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
filename = f"sintactico-{username}-{timestamp}.txt"

parser = yacc.yacc()

with open("logs/"+filename, "w") as file:
    while True:
        try:
            s = input('C# > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)
        file.write(str(result) + "\n")
    
file.close()