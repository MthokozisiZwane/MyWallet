#This is for all my routes in the website
from flask import render_template, redirect, url_for, request, Blueprint, flash
from website.models import Income, Expense, db, Budget
from flask_login import login_required, current_user
from sqlalchemy import extract
from flask import jsonify


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template('home.html',user=current_user)

# add or set a budget
def set_budget(user_id, category, amount):

    # Check if a budget already exists for the given category and user
    existing_budget = Budget.query.filter_by(user_id=user_id, category=category).first()
    if existing_budget:
        # Update the existing budget
        existing_budget.amount = amount
    else:
        # Create a new budget entry
        new_budget = Budget(user_id=user_id, category=category, amount=amount)
        db.session.add(new_budget)
    db.session.commit()

# get or view your budget from database
def get_budget(user_id, category):
    budget = Budget.query.filter_by(user_id=user_id, category=category).first()
    return budget


# function or method to update your budget
def update_budget(user_id, category, new_amount):
    pass # implemented in set_budget

#function to delete your budget
def delete_budget(user_id, category):
    budget = Budget.query.filter_by(user_id=user_id, category=category).first()
    if budget:
        db.session.delete(budget)
        db.session.commit()


# Generate monthly report

def generate_monthly_report(user_id, year, month):
    # Retrieve income entries for the specified month and year
    incomes = Income.query.filter(
        extract('year', Income.date) == year,
        extract('month', Income.date) == month,
        Income.user_id == user_id
    ).all()

    # Retrieve expense entries for the specified month and year
    expenses = Expense.query.filter(
        extract('year', Expense.date) == year,
        extract('month', Expense.date) == month,
        Expense.user_id == user_id
    ).all()

    # Retrieve budget entries for the specified month and year
    budgets = Budget.query.filter(
        Budget.user_id == user_id
    ).all()

    # Calculate totals for income, expenses, and budgets
    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    total_budget = sum(budget.amount for budget in budgets)

    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_budget': total_budget,
        'incomes': incomes,
        'expenses': expenses,
        'budgets': budgets
    }


# function to add income entry
@views.route('/add_income', methods=['POST'])
@login_required
def add_income():

    amount = request.form.get('amount')
    category = request.form.get('category')
    description = request.form.get('description')
    date = request.form.get('date')

    if not (amount and category and date):
        flash('Please fill in all required fields for income.', 'error')
        return redirect(url_for('views.home'))

    new_income = Income(amount=amount, date=date, category=category, user_id=current_user.id)
    db.session.add(new_income)
    db.session.commit()

    flash('Income added successfully.', 'success')
    return redirect(url_for('views.home'))


# function to add expense entry
@views.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    amount = request.form.get('amount')
    category = request.form.get('category')
    description = request.form.get('description')
    date = request.form.get('date')

    if not (amount and category and date):
        flash('Please fill in all required fields for expense.', 'error')
        return redirect(url_for('views.home'))

    new_expense = Expense(amount=amount, date=date, category=category, user_id=current_user.id)
    db.session.add(new_expense)
    db.session.commit()

    flash('Expense added successfully.', 'success')
    return redirect(url_for('views.home'))


# function to delete income entry
@views.route('/delete_income/<int:entry_id>', methods=['POST'])
@login_required
def delete_income(entry_id):
    income_to_delete = Income.query.get(entry_id)
    if income_to_delete and income_to_delete.user_id == current_user.id:
        db.session.delete(income_to_delete)
        db.session.commit()
        flash('Income deleted successfully.', 'success')
    else:
        flash('Income not found or you do not have permission to delete it.', 'error')
    return redirect(url_for('views.home'))

# function to delete expense entry
@views.route('/delete_expense/<int:entry_id>', methods=['POST'])
@login_required
def delete_expense(entry_id):
    expense_to_delete = Expense.query.get(entry_id)
    if expense_to_delete and expense_to_delete.user_id == current_user.id:
        db.session.delete(expense_to_delete)
        db.session.commit()
        flash('Expense deleted successfully.', 'success')
    else:
        flash('Expense not found or you do not have permission to delete it.', 'error')
    return redirect(url_for('views.home'))

@views.route('/income_expense')
@login_required
def income_expense():
    return render_template('income_expense.html')

@views.route('/monthly_report')
@login_required
def monthly_report():
    return render_template('monthly_report.html')


@views.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user)

# budget routes
#from flask import request

# Set Budget Route
@views.route('/set_budget', methods=['POST'])
@login_required
def set_budgets():
    if request.method == 'POST':
        user_id = current_user.id
        category = request.form.get('category')
        amount_str = request.form.get('amount')
        if amount_str is not None:
            amount = float(amount_str)
            set_budget(user_id, category, amount)
        return redirect(url_for('views.dashboard'))
    return redirect(url_for('views.dashboard'))


# Update Budget Route
@views.route('/update_budget/<string:category>', methods=['POST'])
@login_required
def update_budgets(category):
    if request.method == 'POST':
        user_id = current_user.id
        new_amount_str = request.form.get('new_amount')
        if new_amount_str is not None:
            new_amount = float(new_amount_str)
            update_budget(user_id, category, new_amount)
        return redirect(url_for('views.dashboard'))
    return redirect(url_for('views.dashboard'))


# Delete Budget Route
@views.route('/delete_budget/<string:category>', methods=['POST'])
@login_required
def delete_budgets(category):
    if request.method == 'POST':
        user_id = current_user.id
        delete_budget(user_id, category)
        return redirect(url_for('views.dashboard'))
    return redirect(url_for('views.dashboard'))


# Route for generating the monthly report
@views.route('/generate_monthly_report', methods=['POST'])
@login_required
def generate_monthly_reports():
    if request.method == 'POST':
        year = request.form.get('year')
        month = request.form.get('month')
        user_id = current_user.id
        report_data = generate_monthly_report(user_id, year, month)
        return jsonify(report_data)
        return render_template('monthly_report.html', **report_data)
    return jsonify({'error': 'Method not allowed'}), 405