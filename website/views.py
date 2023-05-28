from flask import Blueprint, render_template, request, redirect, url_for
from .models import Payment
from . import db
from datetime import date
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/dashboard', methods=['GET'])
@login_required
def dashboard():

    curr_month = date.today().month
    curr_year = date.today().year

    #SELECT * FROM payment WHERE user_id == current_user.id AND date BETWEEN ? and ?
    query_payments = db.session.query(Payment).filter(Payment.user_id == current_user.id, Payment.date.between(date(curr_year, curr_month, 1), date(curr_year, curr_month, 31)))

    #SELECT payment_category, SUM(amount) FROM payment WHERE user_id == ? AND payment_type == "EXPENSE" GROUP BY payment_category 
    query_expenses = db.session.query(Payment.payment_category, db.func.sum(Payment.amount).label("amount")).filter(Payment.user_id == current_user.id, Payment.payment_type == "EXPENSE", Payment.date.between(date(curr_year, curr_month, 1), date(curr_year, curr_month, 31)))
    #SELECT payment_category, sum(INCOME) FROM income_expense WHERE USER_ID=? AND date BETWEEN ? and ? GROUP BY CATEGORY
    query_incomes = db.session.query(Payment.payment_category, db.func.sum(Payment.amount).label("amount")).filter(Payment.user_id == current_user.id, Payment.payment_type == "INCOME", Payment.date.between(date(curr_year, curr_month, 1), date(curr_year, curr_month, 31)))

    for row in query_expenses:
        expense_pie_labels = [row.payment_category]
        expense_pie_values = [row.amount]

    for row in query_incomes:
        income_pie_labels = [row.payment_category]
        income_pie_values = [row.amount]    

    return render_template("dashboard.html",payments=query_payments, user=current_user, ex_pie_labels=expense_pie_labels
                                            ,ex_pie_values=expense_pie_values, in_pie_labels=income_pie_labels ,
                                             in_pie_values=income_pie_values)


@views.route('/insert_to_db', methods=['POST'])
def insert_to_db():

    date_obj = date.fromisoformat(request.form.get('date'))
    payment_type = request.form.get('payment_type')
    payment_category = request.form.get('payment_category')
    amount = request.form.get('amount')

    payment = Payment(date=date_obj,
                    payment_type=payment_type,
                    payment_category=payment_category,
                    amount=amount,
                    user_id = current_user.id)

    db.session.add(payment)
    db.session.commit()

    return redirect(url_for('views.dashboard'))