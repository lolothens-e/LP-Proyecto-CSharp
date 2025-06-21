// Archivo de prueba: test_avanzado.cs
// Este archivo prueba la sintaxis que tu parser ya debería entender,
// combinando funciones, aritmética y lógica.

// --- PRUEBA 1: Definición de función y aritmética simple ---
// Objetivo: Verificar que las asignaciones y operaciones básicas funcionan.
void pruebaAritmeticaSimple() {
    int a = 10;
    int b = 20;
    int c = a + b;      // Suma
    c = b - 5;        // Resta con re-asignación
    int d = c * -2;     // Multiplicación con operador unario (negativo)
    d = b / 10;       // División
    int e = 21 % 4;     // Módulo
}

// --- PRUEBA 2: Precedencia de operadores aritméticos ---
// Objetivo: Asegurar que el parser respeta el orden matemático correcto.
void pruebaPrecedenciaAritmetica() {
    int resultado_uno = 5 + 3 * 2;      // Debe interpretarse como 5 + (3 * 2) = 11
    int resultado_dos = (5 + 3) * 2;      // Debe interpretarse como (5 + 3) * 2 = 16
    int complejo = 100 - 40 / (5 + 5);  // Debe ser 100 - (40 / 10) = 96
}

// --- PRUEBA 3: Condiciones lógicas y sentencias IF ---
// Objetivo: Probar los operadores lógicos, de comparación y la estructura 'if'.
void pruebaCondiciones() {
    bool simple = true;
    bool compuesto = false || true && false; // Debe ser false || (true && false) -> false
    bool comparacion = 100 > 50;

    // Prueba de un IF simple con una variable
    if (comparacion) {
        // Cuerpo del if, puede estar vacío
    }

    // Prueba de NOT y operadores de comparación
    if (!false && 20 <= 20) {
        int local = 1; // Prueba de declaración dentro de un bloque
    }
}

// --- PRUEBA 4: Integración Completa (La prueba de fuego) ---
// Objetivo: Combinar todo para simular un fragmento de programa más realista.
int pruebaFinalIntegracion() {
    int puntaje = 75;
    int velocidad = 100;
    int penalidad = 5 * (velocidad / 10); // penalidad = 5 * 10 = 50

    bool esGanador = puntaje - penalidad > 20; // 75 - 50 > 20 -> 25 > 20 -> true

    // Condición compleja anidada
    if (esGanador && (puntaje > 50 || velocidad < 90)) {
        // La condición es: true && (true || false) -> true
        
    }
}