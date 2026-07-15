// calculations.js
// Gestion des calculs des notes de frais

// calcul d'un déplacement
export function calculateTravel(card) {

    const km = parseFloat(
        card.querySelector(".kilometers")?.value || 0
    );
    const kmRate = parseFloat(
        card.querySelector(".km-rate")?.value || 0
    );
    const toll = parseFloat(
        card.querySelector(".toll-amount")?.value || 0
    );
    const other = parseFloat(
        card.querySelector(".other-amount")?.value || 0
    );
    const isElectric =
        card.querySelector(".electric-vehicle")?.checked || false;
    // montant kilométrique
    let kilometerAmount = km * kmRate;
    // majoration véhicule électrique
    if (isElectric) {
        kilometerAmount *= 1.20;
    }
    // montant total
    const amount =
        kilometerAmount +
        toll +
        other;
    const amountInput =
        card.querySelector(".amount");
    if (amountInput) {
        amountInput.value = amount.toFixed(2);
    }
}

// calcul d'une ligne
export function calculateCard(card) {

    const itemTypeInput =
        card.querySelector(".item-type");
    if (!itemTypeInput) {
        console.error(
            "Type de dépense introuvable",
            card
        );
        return;
    }
    switch (itemTypeInput.value) {
        case "KM":
            calculateTravel(card);
            break;
        case "REPAS":
        case "FOURNITURE":
        case "HOTEL":
        case "OTHER":
            break;
        default:
            console.warn(
                "Type de dépense inconnu :",
                itemTypeInput.value
            );
    }
}

// calcul du total
export function calculateTotal(totalElement) {

    let total = 0;
    document
        .querySelectorAll(".amount")
        .forEach(function (input) {
            total +=
                parseFloat(input.value) || 0;
        });
    if (totalElement) {
        totalElement.textContent =
            total.toFixed(2) + " €";
    }
}

// recalcul global

export function refresh(totalElement) {
    document
        .querySelectorAll(".expense-item")
        .forEach(function (card) {
            calculateCard(card);
        });
    calculateTotal(totalElement);
}
