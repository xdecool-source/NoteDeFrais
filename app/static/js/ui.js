// ui.js
// Gestion de l'interface utilisateur

import { refresh } from "./calculations.js";

/**
 * Filtre le menu "Ajouter une dépense"
 */
export function filterExpenseMenu(currentExpenseType) {

    const buttons = [
        {
            id: "btn-add-item",
            type: "KM"
        },
        {
            id: "btn-add-meal",
            type: "REPAS"
        },
        {
            id: "btn-add-supplies",
            type: "FOURNITURE"
        },
        {
            id: "btn-add-hotel",
            type: "HOTEL"
        },
        {
            id: "btn-add-other",
            type: "OTHER"
        }
    ];

    buttons.forEach(function (button) {
        const element =
            document.getElementById(button.id);
        if (!element) {
            return;
        }
        const line =
            element.closest("li");
        if (!line) {
            return;
        }
        if (
            currentExpenseType === null ||
            currentExpenseType === button.type
        ) {
            line.style.display = "";
        }
        else {

            line.style.display = "none";
        }
    });
}

/**
 * Ajoute une dépense
 */
export function addExpenseItem(
    templateId,
    itemType,
    currentExpenseType,
    setCurrentExpenseType,
    container,
    totalElement
) {

    // Première dépense
    if (currentExpenseType === null) {
        setCurrentExpenseType(itemType);
        filterExpenseMenu(itemType);
    }
    const template =
        document.getElementById(templateId);
    if (!template) {
        console.error(
            "Template introuvable :",
            templateId
        );
        return;
    }
    const clone =
        template.content.cloneNode(true);
    container.prepend(clone);
    refresh(totalElement);
}

