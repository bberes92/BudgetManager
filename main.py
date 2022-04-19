from flask import Flask, render_template, request, redirect, session, url_for
from datetime import date
from DB.database import BudgetManager as db

app = Flask(__name__)
app.secret_key = "mysecretkey123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        dao = db()
        user = dao.get_user_by_email(email)
        
        if user is not None and user[2] == password:
            session["user_name"] = user[3]
            session["user_id"] = user[0]
            return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        balance = request.form["balance"]
        user = (email, password, username, balance)

        dao = db()
        dao.insert_user(user)

        return redirect(url_for("login"))

    return render_template("sign_up.html")

@app.route("/log_out")
def log_out():
    session["user_name"] = ""
    session["user_id"] = ""

    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    
    dao = db()
    user_id = session.get("user_id")
    user_name = session.get("user_name")
    curr_balance = dao.get_user_balance(user_id)

    if request.method == 'POST':
        from_date = request.form["from_date_input"]
        to_date = request.form["to_date_input"]
    
    if request.method == "GET":
        from_date = date.today().replace(day=1)
        to_date = date.today()

    data = dao.get_user_data(user_id, from_date, to_date)

    income = [item[3] for item in data if item[3] != ""]
    total_income = sum(income)

    expense = [item[4] for item in data if item[4] != ""]
    total_expense = sum(expense)

    expense_pie_data = dao.get_expenses_by_category(user_id, from_date, to_date)
    expense_pie_labels = [item[0] for item in expense_pie_data]
    expense_pie_values = [item[1] for item in expense_pie_data]

    income_pie_data = dao.get_income_by_category(user_id, from_date, to_date)
    income_pie_labels = [item[0] for item in income_pie_data]
    income_pie_values = [item[1] for item in income_pie_data]


    return render_template("dashboard.html",data=data, 
                                            from_date=from_date, 
                                            to_date=to_date, 
                                            user_name=user_name,
                                            curr_balance=curr_balance,
                                            ex_pie_labels=expense_pie_labels,
                                            ex_pie_values=expense_pie_values,
                                            in_pie_labels=income_pie_labels,
                                            in_pie_values=income_pie_values,
                                            total_income=total_income,
                                            total_expense=total_expense)

@app.route("/graphs")
def graphs():

    user_id = session.get("user_id")
    today_date = date.today()
    month_start_date = today_date.replace(day=1)
    month_end_date = today_date.replace(day=31)
    year_back_date = today_date.replace(year=today_date.year - 1)
    
    dao = db()

    expense_pie_data = dao.get_expenses_by_category(user_id, month_start_date, month_end_date)
    expense_pie_labels = [item[0] for item in expense_pie_data]
    expense_pie_values = [item[1] for item in expense_pie_data]

    income_pie_data = dao.get_income_by_category(user_id, month_start_date, month_end_date)
    income_pie_labels = [item[0] for item in income_pie_data]
    income_pie_values = [item[1] for item in income_pie_data]

    monthly_expense_data = dao.get_monthly_expense(user_id, year_back_date, month_end_date)
    monthly_expense_labels = [item[0] for item in monthly_expense_data]
    monthly_expense_values = [item[1] for item in monthly_expense_data]

    return render_template("graphs.html", 
                            ex_pie_labels=expense_pie_labels,
                            ex_pie_values=expense_pie_values,
                            in_pie_labels=income_pie_labels,
                            in_pie_values=income_pie_values,
                            bar_monthly_labels=monthly_expense_labels,
                            bar_monthly_values=monthly_expense_values)

@app.route("/add_to_db", methods=["POST"])
def add_to_db():

    dao = db()
    date = request.form["date_input"]
    transaction_type = request.form["type_select"]
    category = request.form["category"]
    sum = request.form["sum_input"]
    user_id = session.get("user_id")
    curr_balance = dao.get_user_balance(user_id)

    if(transaction_type == "INCOME"):
        income = sum
        expense = ""
        curr_balance += float(sum)
    
    if(transaction_type == "EXPENSE"):
        income = ""
        expense = sum 
        curr_balance -= float(sum)
    
    item = (date, category, income, expense, user_id)

    
    dao.insert(item)
    dao.update_user_balance(user_id, curr_balance)

    return redirect(url_for("dashboard"))   

if __name__ == '__main__':
    app.run()
