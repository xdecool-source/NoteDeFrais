// soumission d'une note

const submitButton =
    document.getElementById("btn-submit-expense");


if (submitButton) {
    submitButton.addEventListener(
        "click",
        async function () {
            const expenseId =
                submitButton.dataset.expenseId;
            const confirmation =
                confirm(
                    "Voulez-vous soumettre cette note de frais ?"
                );
            if (!confirmation) {
                return;
            }
            try {
                const response =
                    await fetch(
                        "/expenses/" + expenseId + "/submit",
                        {
                            method: "POST",
                            credentials: "same-origin",
                            headers: {
                                "Content-Type": "application/json",
                                "X-Requested-With": "XMLHttpRequest"
                            }
                        }
                    );
                if (!response.ok) {
                    const error =
                        await response.text();
                    console.error(error);
                    throw new Error(
                        "Erreur lors de la soumission"
                    );
                }
                window.location.reload();
            }
            catch (error) {
                console.error(error);
                alert(
                    "Impossible de soumettre la note de frais."
                );
            }
        }
    );
}
// validation d'une note


const approveButton =
    document.getElementById("btn-approve-expense");


if (approveButton) {
    approveButton.addEventListener(
        "click",
        async function () {
            const expenseId =
                approveButton.dataset.expenseId;
            const confirmation =
                confirm(
                    "Voulez-vous valider cette note de frais ?"
                );
            if (!confirmation) {
                return;
            }
            try {
                const response =
                    await fetch(
                        "/expenses/" + expenseId + "/approve",
                        {
                            method: "POST",
                            credentials: "same-origin",
                            headers: {
                                "Content-Type": "application/json",
                                "X-Requested-With": "XMLHttpRequest"
                            }
                        }
                    );
                if (!response.ok) {
                    const error =
                        await response.text();
                    console.error(error);
                    throw new Error(
                        "Erreur lors de la validation"
                    );
                }
                window.location.reload();
            }
            catch (error) {
                console.error(error);
                alert(
                    "Impossible de valider la note de frais."
                );
            }
        }
    );
}
// refus d'une note


const rejectButton =
    document.getElementById("btn-reject-expense");
const confirmRejectButton =
    document.getElementById("btn-confirm-reject");
const rejectionReason =
    document.getElementById("rejection-reason");
const rejectionError =
    document.getElementById("rejection-error");
// ouverture de la modale de refus


if (rejectButton) {
    rejectButton.addEventListener(
        "click",
        function () {
            rejectionReason.value = "";
            rejectionError.classList.add("d-none");
            const modalElement =
                document.getElementById(
                    "rejectExpenseModal"
                );
            const rejectModal =
                bootstrap.Modal.getOrCreateInstance(
                    modalElement
                );
            rejectModal.show();
        }
    );
}
// confirmation du refus


if (confirmRejectButton) {
    confirmRejectButton.addEventListener(
        "click",
        async function () {
            const reason =
                rejectionReason.value.trim();
            if (reason.length < 3) {
                rejectionError.classList.remove(
                    "d-none"
                );
                return;
            }
            rejectionError.classList.add(
                "d-none"
            );
            const expenseId =
                rejectButton.dataset.expenseId;
            try {
                const response =
                    await fetch(
                        "/expenses/"
                        + expenseId
                        + "/reject",
                        {
                            method: "POST",
                            credentials:
                                "same-origin",
                            headers: {
                                "Content-Type": "application/json",
                                "X-Requested-With": "XMLHttpRequest"
                            },
                            body:
                                JSON.stringify({
                                    rejection_reason:
                                        reason
                                })
                        }
                    );
                if (!response.ok) {
                    const errorText =
                        await response.text();
                    console.error(
                        "Erreur serveur :",
                        errorText
                    );
                    throw new Error(
                        "Erreur lors du refus"
                    );
                }
                window.location.reload();
            }
            catch (error) {
                console.error(error);
                alert(
                    "Impossible de refuser la note de frais."
                );
            }
        }
    );
}
// remboursement d'une note

const payButton =
    document.getElementById("btn-pay-expense");


if (payButton) {
    payButton.addEventListener(
        "click",
        async function () {
            const expenseId =
                payButton.dataset.expenseId;
            const confirmation =
                confirm(
                    "Voulez-vous marquer cette note comme payée ?"
                );
            if (!confirmation) {
                return;
            }
            try {
                const response =
                    await fetch(
                        "/expenses/" + expenseId + "/pay",
                        {
                            method: "POST",
                            credentials: "same-origin",
                            headers: {
                                "Content-Type": "application/json",
                                "X-Requested-With": "XMLHttpRequest"
                            }
                        }
                    );
                if (!response.ok) {
                    const error =
                        await response.text();
                    console.error(error);
                    throw new Error(
                        "Erreur lors du remboursement"
                    );
                }
                window.location.reload();
            }
            catch (error) {
                console.error(error);
                alert(
                    "Impossible de marquer la note comme payée."
                );
            }
        }
    );
}
// upload des justificatifs


document.addEventListener(
    "click",
    async function (event) {
        const button =
            event.target.closest(
                ".btn-upload-receipt"
            );
        if (!button) {
            return;
        }
        const expenseId =
            button.dataset.expenseId;
        const itemId =
            button.dataset.itemId;
        const container =
            button.closest(
                ".receipt-container"
            );
        const fileInput =
            container.querySelector(
                ".receipt-file"
            );
        const message =
            container.querySelector(
                ".receipt-message"
            );
        if (!fileInput.files.length) {
            message.innerHTML =
                '<span class="text-danger">'
                + 'Sélectionnez un fichier.'
                + '</span>';
            return;
        }
        const file =
            fileInput.files[0];
        const formData =
            new FormData();
        formData.append(
            "file",
            file
        );
        button.disabled = true;
        button.textContent =
            "Envoi...";
        message.innerHTML =
            '<span class="text-muted">'
            + 'Envoi du justificatif...'
            + '</span>';
        try {
            const response =
                await fetch(
                    "/expenses/"
                    + expenseId
                    + "/items/"
                    + itemId
                    + "/receipts",
                    {
                        method: "POST",
                        credentials: "same-origin",
                        headers: {
                            "X-Requested-With": "XMLHttpRequest"
                        } ,
                        body: formData
                    }
                );
            if (!response.ok) {
                const error =
                    await response.json();
                throw new Error(
                    error.detail
                    ||
                    "Erreur lors de l'envoi"
                );
            }
            fileInput.value = "";
            window.location.reload();
        }
        catch (error) {
            console.error(error);
            message.innerHTML =
                '<span class="text-danger">'
                + error.message
                + '</span>';
        }
        finally {
            button.disabled = false;
            button.textContent =
                "Ajouter";
        }
    }
);
// suppression d'un justificatif


document.addEventListener(
    "click",
    async function (event) {
        const button =
            event.target.closest(
                ".btn-delete-receipt"
            );
        if (!button) {
            return;
        }
        const confirmation =
            confirm(
                "Voulez-vous supprimer ce justificatif ?"
            );
        if (!confirmation) {
            return;
        }
        const expenseId =
            button.dataset.expenseId;
        const receiptId =
            button.dataset.receiptId;
        button.disabled = true;
        button.textContent =
            "Suppression...";
        try {
            const response =
                await fetch(
                    "/expenses/"
                    + expenseId
                    + "/receipts/"
                    + receiptId,
                    {
                        method: "DELETE",
                        credentials:
                            "same-origin",
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
                    ||
                    "Erreur lors de la suppression"
                );
            }
            window.location.reload();
        }
        catch (error) {
            console.error(error);
            alert(
                error.message
            );
            button.disabled = false;
            button.textContent =
                "Supprimer";
        }
    }
);
