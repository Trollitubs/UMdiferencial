const API_URL = "http://127.0.0.1:8000/api/v1/solve-derivative";

const mathInput = document.getElementById("math-input");
const mathPreview = document.getElementById("math-preview");
const solveBtn = document.getElementById("solve-btn");
const resultsSection = document.getElementById("results-section");
const stepsList = document.getElementById("steps-list");

// ==========================================
// 1. VISTA PREVIA EN TIEMPO REAL (Live Preview)
// ==========================================
mathInput.addEventListener("input", updateLivePreview);

function updateLivePreview() {
    const rawInput = mathInput.value.trim();

    if (!rawInput) {
        katex.render("\\text{Escribe una función arriba...}", mathPreview, { throwOnError: false });
        return;
    }

    // Convertidor rápido de sintaxis plana a LaTeX para previsualización
    let latexFormatted = formatRawToLatex(rawInput);

    try {
        katex.render(latexFormatted, mathPreview, {
            throwOnError: false,
            displayMode: true
        });
    } catch (e) {
        mathPreview.textContent = rawInput;
    }
}

// Función auxiliar para formatear la entrada del usuario a LaTeX borrador
function formatRawToLatex(expr) {
    return expr
        .replace(/\*/g, " \\cdot ")
        .replace(/sin/g, "\\sin")
        .replace(/cos/g, "\\cos")
        .replace(/tan/g, "\\tan")
        .replace(/sqrt\(([^)]+)\)/g, "\\sqrt{$1}")
        .replace(/\^([\w\d]+|\([^)]+\))/g, "^{$1}");
}

// ==========================================
// 2. PETICIÓN HTTP AL BACKEND (Calcular)
// ==========================================
solveBtn.addEventListener("click", calculateDerivative);
mathInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") calculateDerivative();
});

async function calculateDerivative() {
    const expression = mathInput.value.trim();

    if (!expression) {
        alert("Por favor ingresa una función para derivar.");
        return;
    }

    solveBtn.disabled = true;
    solveBtn.textContent = "Calculando...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                expression: expression,
                variable: "x"
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Error en el servidor");
        }

        const steps = await response.json();
        renderSteps(steps);

    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        solveBtn.disabled = false;
        solveBtn.textContent = "Calcular Paso a Paso";
    }
}

// Función auxiliar para renderizar fórmulas inline $...$ dentro de textos
function renderInlineKaTeX(text) {
    return text.replace(/\$([^$]+)\$/g, (match, latexCode) => {
        try {
            return katex.renderToString(latexCode, {
                throwOnError: false,
                displayMode: false
            });
        } catch (e) {
            return match;
        }
    });
}

function renderSteps(steps) {
    stepsList.innerHTML = "";
    resultsSection.classList.remove("hidden");

    steps.forEach(step => {
        const card = document.createElement("div");
        card.className = "step-card";

        // Convertir variables tipo $x$ o $2$ en KaTeX real dentro de la explicación
        const formattedExplanation = renderInlineKaTeX(step.explanation);

        card.innerHTML = `
            <div class="step-header">
                <span class="step-number">Paso ${step.step_number}</span>
                <span class="rule-badge">${step.rule_name}</span>
            </div>
            <div class="step-explanation">${formattedExplanation}</div>
            <div class="step-math" id="step-math-${step.step_number}"></div>
        `;

        stepsList.appendChild(card);

        // Renderizar el bloque LaTeX con el operador d/dx
        const mathContainer = document.getElementById(`step-math-${step.step_number}`);
        katex.render(step.expression_latex, mathContainer, {
            displayMode: true,
            throwOnError: false
        });
    });

    resultsSection.scrollIntoView({ behavior: "smooth" });
}