//
//
//


export async function loadReceipts(expenseId, itemId) {
    const response =
        await fetch(
            `/expenses/${expenseId}/items/${itemId}/receipts`,
            {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        );
    if (!response.ok) {
        throw new Error(
            "Erreur lors du chargement des justificatifs."
        );
    }
    return await response.json();
}

export async function deleteReceipt(expenseId, receiptId) {
    const response =
        await fetch(
            `/expenses/${expenseId}/receipts/${receiptId}`,
            {
                method: "DELETE",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        );
    if (!response.ok) {
        throw new Error(
            "Impossible de supprimer le justificatif."
        );
    }
    return await response.json();
}

