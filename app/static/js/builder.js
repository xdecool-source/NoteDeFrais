// builder.js

export function buildExpense() {

    const expense = {
        expense_date:
            document
                .getElementById("expense_date")
                .value,
        label:
            document
                .getElementById("label")
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
                        .querySelector(".item-type")
                        .value,
                description:
                    card
                        .querySelector(".description")
                        ?.value || null,
                departure:
                    card
                        .querySelector(".departure")
                        ?.value || null,
                arrival:
                    card
                        .querySelector(".arrival")
                        ?.value || null,
                kilometers:
                    parseFloat(
                        card
                            .querySelector(".kilometers")
                            ?.value || 0
                    ),
                is_electric_vehicle:
                    card
                        .querySelector(".electric-vehicle")
                        ?.checked || false,
                km_rate:
                    parseFloat(
                        card
                            .querySelector(".km-rate")
                            ?.value || 0
                    ),
                toll_amount:
                    parseFloat(
                        card
                            .querySelector(".toll-amount")
                            ?.value || 0
                    ),
                other_amount:
                    parseFloat(
                        card
                            .querySelector(".other-amount")
                            ?.value || 0
                    ),
                amount:
                    parseFloat(
                        card
                            .querySelector(".amount")
                            ?.value || 0
                    )
            };
            expense.items.push(item);
        });
    return expense;
}
