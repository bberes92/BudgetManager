const income_categories = ["Salary", "Scholarship"]
const expense_categories = ["Food", "Bill", "Shopping", "Rent", "Mortgage"]

function fill_category_options(val) {
    if(val == "INCOME") {
        income_selected()
    };

    if(val == "EXPENSE") {
        expense_selected();
    };
};

function income_selected(){

    let category_selector = document.querySelector("#payment_category");
    category_selector.options.length = 1;

    for(let i = 0; i < income_categories.length; i++){
        category_selector.options.add(new Option(income_categories[i], income_categories[i]));
    };
};

function expense_selected(){

    let category_selector = document.querySelector("#payment_category");
    category_selector.options.length = 1;

    for(let i = 0; i < expense_categories.length; i++){
        category_selector.options.add(new Option(expense_categories[i], expense_categories[i]));
    };
};