/**
 * Gestion de l'affichage des justificatifs.
 */

/**
 * Affiche la liste des justificatifs.
 */
export function displayReceipts(
    receipts,
    expenseId
) {

    const receiptList =
        document.getElementById(
            "receipt-list"
        );

    if (!receiptList) {
        return;
    }

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
            title="Voir">

            👁

        </a>

        <button
            type="button"
            class="btn btn-outline-danger delete-receipt"
            data-receipt-id="${receipt.id}"
            title="Supprimer">

            🗑

        </button>

    </div>

</li>

`;

    });

    html += "</ul>";

    receiptList.innerHTML =
        html;

}

/**
 * Met à jour le compteur de justificatifs.
 */
export function updateReceiptCount(
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