"use strict";

document.addEventListener("DOMContentLoaded", function() {
    // Referencias a los elementos del DOM
    const checkButton = document.getElementById("btn-Check");
    const codeInput = document.getElementById("codeInput");
    
    // Asignar el evento click al botón
    if (checkButton) {
        checkButton.addEventListener("click", analyzeCode);
    }
    
    // Opcional: permitir analizar con Ctrl+Enter
    if (codeInput) {
        codeInput.addEventListener("keydown", function(event) {
            if (event.ctrlKey && event.key === "Enter") {
                analyzeCode();
            }
        });
    }
});

async function analyzeCode() {
    // Referencias a los elementos de resultados
    const lexicalResultEl = document.getElementById("lexical-result");
    const syntaxResultEl = document.getElementById("syntax-result");
    const semanticResultEl = document.getElementById("semantic-result");

    // Reiniciar los resultados a un estado de "cargando"
    lexicalResultEl.textContent = "Analizando...";
    lexicalResultEl.className = "text-yellow-400 text-sm font-normal leading-normal";
    syntaxResultEl.textContent = "Analizando...";
    syntaxResultEl.className = "text-yellow-400 text-sm font-normal leading-normal";
    semanticResultEl.textContent = ""; 
    semanticResultEl.className = "text-red-400 text-sm font-mono leading-normal whitespace-pre-wrap";

    // Leer el contenido del textarea
    const userInput = document.getElementById("codeInput").value;

    if (!userInput.trim()) {
        lexicalResultEl.textContent = "Esperando análisis...";
        lexicalResultEl.className = "text-white text-sm font-normal leading-normal";
        syntaxResultEl.textContent = "Por favor, introduce código para analizar.";
        syntaxResultEl.className = "text-white text-sm font-normal leading-normal";
        semanticResultEl.textContent = "";
        return;
    }

    try {
        // Enviar el dato al backend
        const response = await fetch('/run', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ input: userInput })
        });

        // Convertir la respuesta a JSON
        const data = await response.json();

        // --- Actualizar la interfaz con los resultados ---

        // Resultado Léxico
        if (data.lexical_tokens && data.lexical_tokens.length > 0) {
            lexicalResultEl.textContent = `Éxito (${data.lexical_tokens.length} tokens encontrados)`;
            lexicalResultEl.className = "text-green-400 text-sm font-normal leading-normal";
        } else {
            lexicalResultEl.textContent = "Fallo: No se reconocieron tokens.";
            lexicalResultEl.className = "text-red-400 text-sm font-normal leading-normal";
        }

        // Resultado Sintáctico y Semántico
        if (data.errors && data.errors.length > 0) {
            // Si hay errores, los mostramos
            syntaxResultEl.textContent = `Errores encontrados (${data.errors.length})`;
            syntaxResultEl.className = "text-red-400 text-sm font-normal leading-normal";
            
            // Unimos todos los errores con saltos de línea y los mostramos
            semanticResultEl.textContent = data.errors.join('\n');
        } else {
            // Si no hay errores, mostramos un mensaje de éxito
            syntaxResultEl.textContent = "Sintaxis Correcta";
            syntaxResultEl.className = "text-green-400 text-sm font-normal leading-normal";
            semanticResultEl.textContent = "✅ Análisis semántico exitoso. No se encontraron errores.";
            semanticResultEl.className = "text-green-400 text-sm font-mono leading-normal whitespace-pre-wrap";
        }

    } catch (error) {
        console.error("Error al contactar el servidor:", error);
        syntaxResultEl.textContent = "Error de conexión";
        syntaxResultEl.className = "text-red-400 text-sm font-normal leading-normal";
        semanticResultEl.textContent = "No se pudo conectar con el servidor. Revisa la consola del navegador y asegúrate de que el servidor Flask esté corriendo.";
    }
}