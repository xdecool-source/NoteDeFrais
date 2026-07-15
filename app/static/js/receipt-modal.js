import {
    loadReceipts,
    deleteReceipt
} from "./receipts/api.js";

// =====================================================
// Variables
// =====================================================

let currentExpenseId = null;
let currentItemId = null;

// =====================================================
// Initialisation du modal
// =====================================================

export function initReceiptModal() {

    const modalElement =
        document.getElementById(
            "receiptModal"
        );

    if (!modalElement) {
        return;
    }

    const modal =
        new bootstrap.Modal(
            modalElement
        );

    document.addEventListener(
        "click",
        async function (event) {

            const button =
                event.target.closest(
                    ".manage-receipts"
                );

            if (!button) {
                return;
            }

            currentItemId =
                button.dataset.itemId;

            currentExpenseId =
                document
                    .getElementById(
                        "expense-form"
                    )
                    .dataset
                    .expenseId;

            modal.show();

            await refreshReceipts();

        }
    );

}

// =====================================================
// Rafraîchissement de la liste
// =====================================================

async function refreshReceipts() {

    const receiptList =
        document.getElementById(
            "receipt-list"
        );

    receiptList.innerHTML =
        "Chargement...";

    try {

        const receipts =
            await loadReceipts(
                currentExpenseId,
                currentItemId
            );

        updateReceiptCount(
            currentItemId,
            receipts.length
        );

        displayReceipts(
            receipts,
            currentExpenseId
        );

    }

    catch {

        receiptList.innerHTML =
            `
            <div class="alert alert-danger">

                Erreur de chargement.

            </div>
            `;

    }

}


// =====================================================
// Affichage des justificatifs
// =====================================================

function displayReceipts(
    receipts,
    expenseId
) {

    const receiptList =
        document.getElementById(
            "receipt-list"
        );

    if (!receipts.length) {

        receiptList.innerHTML =
            "<div class='text-muted'>Aucun justificatif.</div>";

        return;

    }

    let html =
        "<ul class='list-group'>";

    receipts.forEach(function (receipt) {

        html += `

<li class="list-group-item d-flex justify-content-between align-items-center">

    <div>

        <div>

            📄 ${receipt.filename}

        </div>

        <div class="small text-muted">

            ${Math.round(receipt.size / 1024)} Ko

        </div>

    </div>

    <div class="btn-group btn-group-sm">

        <a
            class="btn btn-outline-primary"
            href="/expenses/${expenseId}/receipts/${receipt.id}/view"
            target="_blank"
            title="Télécharger">

            Voir

        </a>

        <button
            type="button"
            class="btn btn-outline-danger delete-receipt"
            data-receipt-id="${receipt.id}"
            title="Supprimer">

            Supprimer

        </button>

    </div>

</li>

`;

    });

    html += "</ul>";

    receiptList.innerHTML =
        html;

}


// =====================================================
// Suppression d'un justificatif
// =====================================================

document.addEventListener(
    "click",
    async function (event) {

        const button =
            event.target.closest(
                ".delete-receipt"
            );

        if (!button) {
            return;
        }

        const receiptId =
            button.dataset.receiptId;

        if (
            !confirm(
                "Supprimer ce justificatif ?"
            )
        ) {
            return;
        }

        try {

            await deleteReceipt(
                currentExpenseId,
                receiptId
            );

            await refreshReceipts();

        }

        catch {

            alert(
                "Impossible de supprimer le justificatif."
            );

        }

    }
);

// =====================================================
// Mise à jour du compteur
// =====================================================

function updateReceiptCount(
    itemId,
    count
) {

    const element =
        document.querySelector(
            `.receipt-count[data-item-id="${itemId}"]`
        );

    if (!element) {
        return;
    }

    element.textContent =
        `${count} justificatif(s)`;

}


// =====================================================
// Ajout d'un justificatif
// =====================================================

document.addEventListener(
    "click",
    async function (event) {

        if (
            event.target.id !==
            "upload-receipt"
        ) {
            return;
        }

        const input =
            document.getElementById(
                "receipt-file"
            );

        if (!input.files.length) {

            alert(
                "Sélectionnez un fichier."
            );

            return;

        }

        const uploadButton =
            document.getElementById(
                "upload-receipt"
            );

        uploadButton.disabled = true;
        uploadButton.textContent =
            "Envoi...";

        const formData =
            new FormData();

        formData.append(
            "file",
            input.files[0]
        );

        try {

            const response =
                await fetch(
                    `/expenses/${currentExpenseId}/items/${currentItemId}/receipts`,
                    {
                        method: "POST",
                        body: formData,
                        headers: {
                            "Content-Type": "application/json",
                            "X-Requested-With": "XMLHttpRequest"
                        }
                    }
                );

            if (!response.ok) {

                const error =
                    await response.json();

                throw new Error(
                    error.detail
                );

            }

            input.value = "";

            await refreshReceipts();

        }

        catch (error) {

            alert(
                error.message
            );

        }

        finally {

            uploadButton.disabled = false;

            uploadButton.textContent =
                "📎 Ajouter";

        }

    }
);

