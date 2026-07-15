// constants.js
// Constantes utilisées par les notes de frais

export const EXPENSE_TYPES = {
    KM: "KM",
    REPAS: "REPAS",
    FOURNITURE: "FOURNITURE",
    HOTEL: "HOTEL",
    OTHER: "OTHER"
};

export const EXPENSE_BUTTONS = [
    {
        id: "btn-add-item",
        template: "travel-template",
        type: EXPENSE_TYPES.KM
    },
    {
        id: "btn-add-meal",
        template: "meal-template",
        type: EXPENSE_TYPES.REPAS
    },
    {
        id: "btn-add-supplies",
        template: "supplies-template",
        type: EXPENSE_TYPES.FOURNITURE
    },
    {
        id: "btn-add-hotel",
        template: "hotel-template",
        type: EXPENSE_TYPES.HOTEL
    },
    {
        id: "btn-add-other",
        template: "other-template",
        type: EXPENSE_TYPES.OTHER
    }
];