
import { refresh } from "./calculations.js";
import { buildExpense } from "./builder.js";

export async function saveExpense(event, form, expenseId, totalElement) {
    event.preventDefault();

    const button = form.querySelector('button[type="submit"]');

    if (!button) {
        console.error("Bouton Enregistrer introuvable.");
        return;
    }

    // Empêcher plusieurs enregistrements simultanés
    if (button.dataset.saving === "true") {
        return;
    }

    const originalText = button.textContent.trim() || "Enregistrer";
    const originalClasses = button.className;
    const originalBackground = button.style.backgroundColor;
    const originalColor = button.style.color;

    // Gestion visuelle du bouton
    const setButtonState = (text, color, disabled = true) => {
        button.textContent = text;
        button.style.setProperty("background-color", color, "important");
        button.style.setProperty("border-color", color, "important");
        button.style.setProperty("color", "#FFFFFF", "important");
        button.disabled = disabled;
        button.dataset.saving = disabled ? "true" : "false";
        button.style.cursor = disabled ? "wait" : "pointer";
        button.style.opacity = disabled ? "0.8" : "1";
    };

    // Afficher immédiatement l'état gris
    setButtonState("Enregistrement…", "#9CA3AF", true);

    // Laisser le navigateur afficher le changement
    await new Promise(resolve => requestAnimationFrame(resolve));

    try {
        // Recalcul et préparation des données
        refresh(totalElement);
        const expense = buildExpense();

        let url = "/expenses/";
        let method = "POST";

        if (expenseId) {
            url = `/expenses/${expenseId}`;
            method = "PUT";
        }

        // Enregistrer la note
        const response = await fetch(url, {
            method,
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify(expense)
        });

        if (response.status === 401) {
            setButtonState("Session expirée", "#DC2626", false);
            alert("Votre session a expiré.\nVeuillez vous reconnecter.");
            window.location.href = "/auth/login";
            return;
        }

        if (!response.ok) {
            let detail = "Erreur serveur";

            try {
                const error = await response.json();
                detail = error.detail || detail;
            } catch {}

            throw new Error(detail);
        }

        const result = await response.json();

        if (result.deleted) {
            window.location.href = "/expenses/";
            return;
        }

        // Envoyer les justificatifs après l'enregistrement de la note
        const cards = Array.from(
            document.querySelectorAll(".expense-item")
        );

        const itemIds = result.item_ids || [];
        const uploadErrors = [];

        for (let index = 0; index < cards.length; index++) {
            const card = cards[index];
            const input = card.querySelector(".receipt-files");
            const idInput = card.querySelector(".item-id");

            const existingId = parseInt(idInput?.value, 10) || null;
            const itemId = existingId || itemIds[index];

            // Conserver l'identifiant des nouvelles lignes
            if (!existingId && itemId && idInput) {
                idInput.value = itemId;
            }

            // Aucun justificatif sélectionné pour cette ligne
            if (!input?.files?.length) {
                continue;
            }

            if (!itemId) {
                uploadErrors.push(
                    "Impossible d'identifier une ligne de dépense pour un justificatif."
                );
                continue;
            }

            for (const file of Array.from(input.files)) {
                const data = new FormData();
                data.append("file", file);

                try {
                    const uploadResponse = await fetch(
                        `/expenses/${result.expense_id}/items/${itemId}/receipts`,
                        {
                            method: "POST",
                            credentials: "same-origin",
                            headers: {
                                "X-Requested-With": "XMLHttpRequest"
                            },
                            body: data
                        }
                    );

                    if (!uploadResponse.ok) {
                        let detail = "Erreur lors de l'envoi du fichier.";

                        try {
                            const error = await uploadResponse.json();
                            detail = error.detail || detail;
                        } catch {}

                        uploadErrors.push(`${file.name} : ${detail}`);
                    }
                } catch (error) {
                    uploadErrors.push(
                        `${file.name} : ${error.message}`
                    );
                }
            }
        }

        // La note est enregistrée, mais au moins un justificatif a échoué
        if (uploadErrors.length > 0) {
            setButtonState("Réessayer", "#DC2626", false);

            alert(
                "La note a été enregistrée, mais certains justificatifs n'ont pas pu être envoyés :\n" +
                uploadErrors.join("\n")
            );

            return;
        }

        // Note et justificatifs enregistrés avec succès
        setButtonState("Enregistré ✓", "#16A34A", true);

        // Laisser brièvement voir l'état vert avant la redirection
        await new Promise(resolve => setTimeout(resolve, 500));

        window.location.href = "/expenses/";

    } catch (error) {
        console.error("Erreur lors de l'enregistrement :", error);

        setButtonState("Réessayer", "#DC2626", false);

        alert(error.message || "Une erreur est survenue lors de l'enregistrement.");
    }
}
