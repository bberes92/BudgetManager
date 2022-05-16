const income_categories = ["Salary", "Scholarship"]
const expense_categories = ["Food", "Bill", "Shopping", "Rent", "Mortgage"]

document.addEventListener("DOMContentLoaded", () => {
    income_selected();

});

function add_btn_clicked() {
    const add_btn = document.querySelector(".add-btn");
    const form_container = document.querySelector(".form-container");
    add_btn.style.display = "none";
    form_container.style.display = "block";
};

function cancel_btn_clicked() {
    const add_btn = document.querySelector(".add-btn");
    const form_container = document.querySelector(".form-container");
    add_btn.style.display = "block";
    form_container.style.display = "none";
}

function fill_category_options(val) {
    if(val == "INCOME") {
        income_selected()
    };

    if(val == "EXPENSE") {
        expense_selected();
    };
};

function income_selected(){

    let category_selector = document.querySelector("#select_category");
    category_selector.options.length = 0;

    for(let i = 0; i < income_categories.length; i++){
        category_selector.options.add(new Option(income_categories[i], income_categories[i]));
    };
};

function expense_selected(){

    let category_selector = document.querySelector("#select_category");
    category_selector.options.length = 0;

    for(let i = 0; i < expense_categories.length; i++){
        category_selector.options.add(new Option(expense_categories[i], expense_categories[i]));
    };
};

