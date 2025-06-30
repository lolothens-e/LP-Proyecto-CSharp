using System;
using System.Collections.Generic;
//lacedeno11 algortimo prueba

// Definición de una clase completa
public class TestCompleto
{
    // Campos privados y públicos
    private int _contador = 0;
    public const double PI = 3.14159;
    public string[] mensajes; // Declaración de array

    // Propiedad con get y set
    public int Contador
    {
        get { return _contador; }
        private set { _contador = value; }
    }

    // Constructor de la clase
    public TestCompleto()
    {
        mensajes = new string[5]; // Creación de instancia de array
        _contador++; // Operador de incremento
    }

    // Método principal de ejecución
    public static void Main(string[] args)
    {
        Console.WriteLine("Iniciando prueba...");
        TestCompleto test = new TestCompleto();
        test.EjecutarCiclos(10);
    }

    // Método con bucles y condicionales
    public void EjecutarCiclos(int max)
    {
        // Bucle for y operador de asignación compuesta
        for (int i = 0; i < max; i++)
        {
            if (i % 2 == 0) // Si es par
            {
                Contador += 1;
                Console.WriteLine($"Contador par: {Contador}");
            }
            else
            {
                // Un comentario de una sola línea
                Contador--; // Operador de decremento
            }
        }
        
        // Uso de Diccionario y lambda (como en tu prueba original)
        Dictionary<string, int> puntajes = new Dictionary<string, int>();
        puntajes.Add("lacedeno11", 100);
        
        Func<int, int> alCuadrado = x => x * x;
        int resultadoCuadrado = alCuadrado(Contador);

        Console.WriteLine("Prueba finalizada.");
    }
}