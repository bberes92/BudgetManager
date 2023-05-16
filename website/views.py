from flask import Blueprint, render_template, request
from .models import Payment
from . import db
from datetime import date
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    if request.method == 'POST':
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

    #SELECT payment_category, SUM(amount) FROM payment WHERE user_id == 1 AND payment_type == "EXPENSE" GROUP BY payment_category 
    query_expenses = db.session.query(Payment.payment_category, db.func.sum(Payment.amount).label("amount")).filter(Payment.payment_type == "EXPENSE")
    #SELECT payment_category, sum(INCOME) FROM income_expense WHERE USER_ID=? AND date BETWEEN ? and ? GROUP BY CATEGORY
    query_incomes = db.session.query(Payment.payment_category, db.func.sum(Payment.amount).label("amount")).filter(Payment.payment_type == "INCOME")

    for row in query_expenses:
        expense_pie_labels = [row.payment_category]
        expense_pie_values = [row.amount]

    for row in query_incomes:
        income_pie_labels = [row.payment_category]
        income_pie_values = [row.amount]    

    return render_template("dashboard.html", user=current_user, ex_pie_labels=expense_pie_labels
                                            ,ex_pie_values=expense_pie_values, in_pie_labels=income_pie_labels ,
                                             in_pie_values=income_pie_values)