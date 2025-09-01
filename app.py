from flask import Flask, request, render_template, session, redirect
from sqlalchemy import select,insert
from database import db_session, init_db
import models
import sqlite3

app = Flask(__name__)
app.secret_key = 'qw<ert?yu111io2p"2a3s>.>4d5fghjkl'
INCOME = 1
SPEND = 2

@app.route('/user', methods=['GET', 'DELETE'])
def user_handler():
    print('11111111111111111111111111')
    if request.method == 'GET':
        return 'hello world GET'
    else:
        return 'hello world Delete'


@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        init_db()
        password = request.form['password']
        email = request.form['email']
        data = db_session.execute(select(models.User).filter_by(email=email, password=password)).scalar_one()
        if data:
            session['user_id'] = data.id
            return f'You are in {email} {password}'
        else:
            return f'Wrong password'


@app.route('/register', methods=['GET', 'POST'])
def get_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        init_db()
        username = request.form['username']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        user = models.User(name=username,surname=surname,password=password,email=email)
        db_session.add(user)
        db_session.commit()
        return f'User registered: {username} {password} {email} {surname}'


@app.route('/category', methods=['GET', 'POST'])
def get_all_category():
    if 'user_id' in session:
        init_db()
        if request.method == 'GET':
            data = list(db_session.execute(select(models.Catgeory).filter_by(owner=session['user_id'])).scalars())
            data_system = list(db_session.execute(select(models.Catgeory).filter_by(owner=1)).scalars())
            return render_template("all_category.html", user_categories=data+data_system)
        else:
            category_name = request.form['category_name']
            category_owner = session['user_id']
            new_category = models.Catgeory(name=category_name, owner=category_owner)
            db_session.add(new_category)
            db_session.commit()
            return redirect('/category')
    else:
        return redirect('/login')


@app.route('/category/<category_id>', methods=['GET', 'POST'])
def get_category(category_id):
    if 'user_id' in session:
        init_db()
        if request.method == 'GET':
            transactions = list(db_session.execute(select(models.Transaction).filter_by(category=category_id,owner=session["user_id"])).scalars())
            current_category = list(db_session.execute(select(models.Catgeory).filter_by(id=category_id)).scalars())
            return render_template('one_category.html', category=current_category, transactions=transactions)
        else:
            return 'edit category'
    else:
        return redirect('/login')


@app.route('/category/<category_id>/delete', methods=['GET'])
def delete_category(category_id):
    return f"hello world DELETE {category_id}"


@app.route('/income', methods=['GET', 'POST'])
def get_all_income():
    if 'user_id' in session:
        init_db()
        if request.method == 'GET':
            data = list(db_session.execute(select(models.Transaction).filter_by(owner=session['user_id'],type=INCOME)).scalars())
            return render_template("dashboard.html", transactions=data, dashboard_action='/income')
        else:
                transaction_description = request.form['description']
                transaction_category = request.form['category']
                transaction_amount = request.form['amount']
                transaction_date = request.form['date']
                transaction_owner = session['user_id']
                transaction_type = INCOME
                new_category = models.Transaction(description=transaction_description, category=transaction_category, amount=transaction_amount,date=transaction_date, owner=transaction_owner, type=transaction_type)
                db_session.add(new_category)
                db_session.commit()
                return redirect('/income')
    else:
        return redirect('/login')


@app.route('/income/<income_id>', methods=['GET', 'PATCH', 'DELETE'])
def get_income(income_id):
    if request.method == 'GET':
        return 'category_id'
    elif request.method == 'PATCH':
        return 'PATCH'
    else:
        return 'DLEETE'


@app.route('/spend', methods=['GET', 'POST'])
def get_all_spend():
    if 'user_id' in session:
        init_db()
        if request.method == 'GET':
            data = list(db_session.execute(select(models.Transaction).filter_by(owner=session['user_id'],type=INCOME)).scalars())
            return render_template("dashboard.html", transactions=data, dashboard_action='/spend')
        else:
                transaction_description = request.form['description']
                transaction_category = request.form['category']
                transaction_amount = request.form['amount']
                transaction_date = request.form['date']
                transaction_owner = session['user_id']
                transaction_type = SPEND
                new_category = models.Transaction(description=transaction_description, category=transaction_category, amount=transaction_amount,date=transaction_date, owner=transaction_owner, type=transaction_type)
                db_session.add(new_category)
                db_session.commit()
                return redirect('/spend')
    else:
        return redirect('/login')


@app.route('/spend/<spend_id>', methods=['GET', 'PATCH', 'DELETE'])
def get_spend(spend_id):
    if request.method == 'GET':
        return 'category_id'
    elif request.method == 'PATCH':
        return 'PATCH'
    else:
        return 'DELETE'


if __name__ == '__main__':
    app.run()
