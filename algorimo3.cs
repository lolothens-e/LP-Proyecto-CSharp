using System;
using System.Collections.Generic;

class TestDiccionariosYOperadores
{
    static void Main()
    {
        Dictionary<string, int> puntajes = new Dictionary<string, int>();

        puntajes.Add("lacedeno11", 100);
        
        puntajes["ArielV17"] = 95;
        
        int a = 20;
        int b = 10;
        int resultado;

        resultado = a + b * 2;
        resultado++; 

        a += b; 
        
        if (a >= 30 && resultado != 40)
        {
            bool esCorrecto = true;
        }

        Func<int, int> alCuadrado = x => x * x;
        int numeroAlCuadrado = alCuadrado(b);
    }
}