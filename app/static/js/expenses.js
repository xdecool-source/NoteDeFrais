// NOTES DE FRAIS
// Gestion dynamique des dépenses,
// Calcule les montants et Echange avec l’API.

const form = document.getElementById("expense-form");
const container = document.getElementById("expense-items");
const totalElement = document.getElementById("total");
const expenseId = form.dataset.expenseId || null;

// boutons d'ajout

const addTravelButton =
    document.getElementById("btn-add-item");

const addMealButton =
    document.getElementById("btn-add-meal");

const addSuppliesButton =
    document.getElementById("btn-add-supplies");

const addHotelButton =
    document.getElementById("btn-add-hotel");

const addOtherButton =
    document.getElementById("btn-add-other");


// debug mode

console.log(
    "Mode :",
    expenseId ? "Modification" : "Création"
);

// fonction generique d'ajout

function addExpenseItem(templateId) {

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
    container.appendChild(clone);

    refresh();

}

// evenements des boutons d'ajout

if (addTravelButton) {

    addTravelButton.addEventListener(
        "click",
        function () {
            addExpenseItem(
                "travel-template"
            );
        }
    );
}

if (addMealButton) {

    addMealButton.addEventListener(
        "click",
        function () {
            addExpenseItem(
                "meal-template"
            );
        }
    );
}


if (addSuppliesButton) {

    addSuppliesButton.addEventListener(
        "click",
        function () {
            addExpenseItem(
                "supplies-template"
            );
        }
    );
}

if (addHotelButton) {

    addHotelButton.addEventListener(
        "click",
        function () {
            addExpenseItem(
                "hotel-template"
            );
        }
    );
}


if (addOtherButton) {

    addOtherButton.addEventListener(
        "click",
        function () {
            addExpenseItem(
                "other-template"
            );
        }
    );
}

// suppression d'une ligne

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
        }
        refresh();
    }
);

// modification d'un champ

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
        calculateTotal();
    }
);


// modification d'une case a cocher

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
        calculateTotal();
    }
);

// recalcul global

function refresh() {

    document
        .querySelectorAll(".expense-item")
        .forEach(function (card) {

            calculateCard(card);
        });
    calculateTotal();
}

// calcul d'une carte

function calculateCard(card) {

    const itemTypeInput =
        card.querySelector(".item-type");
    if (!itemTypeInput) {
        console.error(
            "Type de dépense introuvable",
            card
        );
        return;
    }
    const type =
        itemTypeInput.value;
    switch (type) {

        case "KM":
            calculateTravel(card);
            break;
        case "REPAS":
            // Montant saisi manuellement
            break;
        case "FOURNITURE":
            // Montant saisi manuellement
            break;
        case "HOTEL":
            // Montant saisi manuellement
            break;
        case "OTHER":
            // Montant saisi manuellement
            break;
        default:
            console.warn(
                "Type de dépense inconnu :",
                type
            );
            break;
    }
}

// calcul d'un deplacement

function calculateTravel(card) {

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

    // montant kilometrique

    let kilometerAmount =
        km * kmRate;

    // majoration vehicule electrique : + 20 %

    if (isElectric) {

        kilometerAmount =
            kilometerAmount * 1.20;

    }

    // montant total du deplacement

    const amount =
        kilometerAmount
        + toll
        + other;

    // mise a jour du montant

    const amountInput =
        card.querySelector(".amount");
    if (amountInput) {
        amountInput.value =
            amount.toFixed(2);
    }
}

// total de la note

function calculateTotal() {

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

// construction du json




function buildExpense() {

    const expense = {
        expense_date:
            document
                .getElementById(
                    "expense_date"
                )
                .value,
        label:
            document
                .getElementById(
                    "label"
                )
                .value,
        items: []
    };
    document
        .querySelectorAll(".expense-item")
        .forEach(function (card) {
            const item = {
                id:
                    parseInt(
                        card
                            .querySelector(".item-id")
                            ?.value
                    ) || null,
                item_type:
                    card
                        .querySelector(
                            ".item-type"
                        )
                        .value,
                description:
                    card
                        .querySelector(
                            ".description"
                        )
                        ?.value || null,
                departure:
                    card
                        .querySelector(
                            ".departure"
                        )
                        ?.value || null,
                arrival:
                    card
                        .querySelector(
                            ".arrival"
                        )
                        ?.value || null,
                kilometers:
                    parseFloat(
                        card
                            .querySelector(
                                ".kilometers"
                            )
                            ?.value || 0
                    ),
                is_electric_vehicle:
                    card.querySelector(".electric-vehicle")?.checked || false,
                km_rate:
                    parseFloat(
                        card.querySelector(".km-rate")?.value || 0
                    ),
                toll_amount:
                    parseFloat(
                        card
                            .querySelector(
                                ".toll-amount"
                            )
                            ?.value || 0
                ),
                other_amount:
                    parseFloat(
                        card
                            .querySelector(
                                ".other-amount"
                            )
                            ?.value || 0
                    ),
                amount:
                    parseFloat(
                        card
                            .querySelector(
                                ".amount"
                            )
                            ?.value || 0
                    )
            };
            expense.items.push(item);
        });
    return expense;
}

// enregistrement

form.addEventListener(
    "submit",
    saveExpense
);

async function saveExpense(event) {

    event.preventDefault();
    // Recalcul avant enregistrement
    refresh();
    // Construction du JSON
    const expense =
        buildExpense();
    console.log(
        "Données envoyées :",
        expense
    );
    // Création par défaut
    let url =
        "/expenses/";
    let method =
        "POST";
    // Modification
    if (expenseId) {
        url =
            "/expenses/" + expenseId;
        method =
            "PUT";
    }

    try {
        const response =
            await fetch(
                url,
                {
                    method: method,
                    credentials:
                        "same-origin",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body:
                        JSON.stringify(
                            expense
                        )
                }
            );

        if (!response.ok) {

            const error = await response.json();

            throw new Error(
                error.detail || "Erreur serveur"
            );
        }





        const result =
            await response.json();

        if (result.deleted) {
            window.location.href =
                "/expenses/";
            return;
        }
        
        console.log(
            "Réponse serveur :",
            result
        );
        window.location.href =
            "/expenses/";
    }

    catch (error) {

        alert(error.message);

        console.error(error);
    }
}

// initialisation

refresh();
console.log(
    "expenses.js chargé"
);
console.log(
    "expenseId =",
    expenseId
);
