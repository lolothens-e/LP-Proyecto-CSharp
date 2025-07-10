"use strict";

async function sendData() {
    const userInput = document.getElementById("btn-Check").value;
    
    const response = await fetch('/run', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ input: userInput })
    });

    const data = await response.json();
    document.getElementById("output").textContent = data.result;
}