let income_categories = ["Salary", "Scholarship"]
let expense_categories = ["Food", "Bill", "Shopping"]

function income_cheked(){

    let income_radio = document.querySelector("#income");
    let category_selector = document.querySelector("#select_category");
    category_selector.options.length = 0;

    if(income_radio.checked){
        for(let i = 0; i < income_categories.length; i++){
            category_selector.options.add(new Option(income_categories[i], income_categories[i]));
        }
    }
}

function expense_cheked(){

    let expense_radio = document.querySelector("#expense");
    let category_selector = document.querySelector("#select_category");
    category_selector.options.length = 0;

    if(expense_radio.checked){
        for(let i = 0; i < expense_categories.length; i++){
            category_selector.options.add(new Option(expense_categories[i], expense_categories[i]));
        }
    }
}

function add_btn() {

    document.querySelector(".form_container").style.display = "block";
}