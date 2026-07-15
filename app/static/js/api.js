// api.js
// Gestion des appels API des notes de frais

import { refresh } from "./calculations.js";
import { buildExpense } from "./builder.js";

export async function saveExpense(event, form, expenseId, totalElement) {

    event.preventDefault();
    // Recalcul avant enregistrement
    refresh(totalElement);
    // Construction du JSON
    const expense = buildExpense();
    console.log(
        "Données envoyées :",
        expense
    );
    // Création par défaut
    let url = "/expenses/";
    let method = "POST";
    // Modification
    if (expenseId) {
        url = "/expenses/" + expenseId;
        method = "PUT";
    }
    try {
        const response =
            await fetch(
                url,
                {
                    method: method,
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    body: JSON.stringify(expense)
                }
            );

        // Session expirée
        if (response.status === 401) {
            alert("Votre session a expiré.\nVeuillez vous reconnecter.");
            window.location.href = "/auth/login";
            return;
        }


        if (!response.ok) {
            const error =
                await response.json();
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
