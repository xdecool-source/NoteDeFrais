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
