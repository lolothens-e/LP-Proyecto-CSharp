using System;
using System.Collections.Generic;

class TestPrimitivosYArrays
{
    static void Main()
    {
        // Primitivos
        int edad = 30;
        float altura = 1.75f;
        double peso = 72.5;
        bool esEstudiante = true;
        char inicial = 'A';
        string nombre = "Ariel";

        // Arrays
        int[] calificaciones = new int[5];
        string[] nombres = new string[10];

        // Listas
        List<string> amigos = new List<string>();
        List<int> puntajes = new List<int>();

        // Inicialización
        calificaciones[0] = 90;
        amigos.Add("Carlos");
        puntajes.Add(100);
    }
}