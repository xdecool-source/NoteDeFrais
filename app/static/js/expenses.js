// expenses.js
// Point d'entrée de la gestion des notes de frais

import { refresh } from "./calculations.js";
import { filterExpenseMenu } from "./ui.js";
import { initEvents } from "./events.js";
import { EXPENSE_BUTTONS } from "./constants.js";
import { initReceiptModal } from "./receipt-modal.js";

const form =
    document.getElementById("expense-form");
const container =
    document.getElementById("expense-items");
const totalElement =
    document.getElementById("total");
const expenseId =
    form.dataset.expenseId || null;

// Type de la note de frais
let currentExpenseType = null;
console.log(
    "Mode :",
    expenseId
        ? "Modification"
        : "Création"
);

// Initialisation du type si une ligne existe déjà
const firstItem =
    document.querySelector(
        ".expense-item .item-type"
    );
if (firstItem) {
    currentExpenseType =
        firstItem.value;
}

filterExpenseMenu(
    currentExpenseType
);

// Initialisation des événements
initEvents(
    form,
    container,
    totalElement,
    expenseId,
    () => currentExpenseType,
    function (value) {
        currentExpenseType = value;
    },
    EXPENSE_BUTTONS
);

// Justificatifs facultatifs directement dans chaque dépense.
// Les fichiers sont conservés dans le navigateur jusqu'à l'enregistrement.
function ensureReceiptInputs() {
    document.querySelectorAll(".expense-item").forEach((card) => {
        if (card.querySelector(".receipt-files")) return;
        const section = document.createElement("div");
        section.className = "receipt-section mt-3";
        section.innerHTML = `
            <hr>
            <strong>📎 Justificatifs (facultatif)</strong>
            <label class="form-label mt-2">Ajouter un ou plusieurs fichiers</label>
            <input type="file" class="form-control receipt-files"
                   accept=".pdf,.jpg,.jpeg,.png" multiple>
            <div class="form-text">PDF, JPG ou PNG — 10 Mo maximum par fichier. Vous pouvez laisser ce champ vide.</div>
            <div class="small text-muted receipt-pending mt-1"></div>`;
        card.querySelector(".card-body")?.appendChild(section);
    });
}
ensureReceiptInputs();
new MutationObserver(ensureReceiptInputs).observe(container, { childList: true, subtree: true });
initReceiptModal();

// Premier calcul
refresh(totalElement);
console.log(
    "expenses.js chargé"
);
console.log(
    "expenseId =",
    expenseId
);



// Effacer le zéro au premier clic dans Kilomètres, Péage et Divers
document.addEventListener("focusin", function (event) {
    const input = event.target;

    if (
        input.matches(
            "#expense-items .kilometers, " +
            "#expense-items .toll-amount, " +
            "#expense-items .other-amount"
        ) &&
        input.value === "0"
    ) {
        input.value = "";
    }
});


// Effacer le zéro au clic dans le montant des dépenses simples
document.addEventListener("focusin", function (event) {
    const input = event.target;

    if (
        input.matches(
            "#expense-items .expense-item .amount"
        ) &&
        !input.readOnly &&
        input.value === "0"
    ) {
        input.value = "";
    }
});
