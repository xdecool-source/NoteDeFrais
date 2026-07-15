// events.js
// Gestion des événements

import {calculateCard, calculateTotal, refresh} from "./calculations.js";

import {addExpenseItem, filterExpenseMenu} from "./ui.js";

import {saveExpense} from "./api.js";

export function initEvents(
    form,
    container,
    totalElement,
    expenseId,
    getCurrentExpenseType,
    setCurrentExpenseType,
    expenseButtons
) {

    // Boutons d'ajout

    expenseButtons.forEach(function (expenseButton) {
        const button =
            document.getElementById(expenseButton.id);
        if (!button) {
            return;
        }
        button.addEventListener(
            "click",
            function () {
                addExpenseItem(
                    expenseButton.template,
                    expenseButton.type,
                    getCurrentExpenseType(),
                    setCurrentExpenseType,
                    container,
                    totalElement
                );
            }
        );
    });

    // Suppression d'une ligne

    document.addEventListener(
        "click",
        function (event) {
            if (
                !event.target.classList.contains(
                    "delete-item"
                )
            ) {
                return;
            }
            const card =
                event.target.closest(
                    ".expense-item"
                );
            if (card) {
                card.remove();
                const firstItem =
                    document.querySelector(
                        ".expense-item .item-type"
                    );
                if (firstItem) {
                    setCurrentExpenseType(
                        firstItem.value
                    );
                }
                else {
                    setCurrentExpenseType(
                        null
                    );

                }
                filterExpenseMenu(
                    getCurrentExpenseType()
                );
            }

            refresh(totalElement);
        }
    );

    // Modification d'un champ

    document.addEventListener(
        "input",
        function (event) {
            const card =
                event.target.closest(
                    ".expense-item"
                );
            if (!card) {
                return;
            }
            calculateCard(card);
            calculateTotal(totalElement);
        }
    );

    // Modification d'une case à cocher

    document.addEventListener(
        "change",
        function (event) {
            const card =
                event.target.closest(
                    ".expense-item"
                );
            if (!card) {
                return;
            }
            calculateCard(card);
            calculateTotal(totalElement);
        }
    );

    // Enregistrement

    form.addEventListener(
        "submit",
        function (event) {
            saveExpense(
                event,
                form,
                expenseId,
                totalElement
            ); 
        }
    );
}
