from flask import Flask, request, render_template, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'qw<ert?yu111io2p"2a3s>.>4d5fghjkl'
INCOME = 1
SPEND = 2


class DBwrapper:
    def insert(self, table, data):
        with DatabaseManager('financial_tracker.db') as cursor:
            cursor.execute(f"INSERT INTO '{table}' ({', '.join(data.keys())}) VALUES ({', '.join(['?'] * len(data))})",
                           tuple(data.values()))

    def select(self, table, where=None):
        with DatabaseManager('financial_tracker.db') as cursor:
            if where:
                result_params = []
                for k, v in where.items():
                    if isinstance(v,(list,tuple)):
                        result_params.append(f'{k} IN ({", ".join(str(i) for i in v)})')
                    else:
                        if isinstance(v, str):
                            result_params.append(f"{k} = '{v}'")
                        else:
                            result_params.append(f"{k} = {v}")
                result_where = ' AND '.join(result_params)

                cursor.execute(f"SELECT * FROM '{table}' WHERE {result_where}")
            else:
                cursor.execute(f"SELECT * FROM '{table}'")
            return cursor.fetchall()

class DatabaseManager():
    def __init__(self, database_name):
        self.database_name = database_name

    def __enter__(self):
        self.connect = sqlite3.connect(self.database_name)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.commit()
        self.connect.close()


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
        password = request.form['password']
        email = request.form['email']
        db = DBwrapper()
        data = db.select('user', {'email':email, 'password':password})
        if data:
            session['user_id'] = data[0]['id']
            return f'You are in {email} {password}'
        else:
            return f'Wrong password'


@app.route('/register', methods=['GET', 'POST'])
def get_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        db = DBwrapper()
        db.insert('user', {'name':username, 'surname':surname,'password':password,'email':email})
        return f'User registered: {username} {password} {email} {surname}'


@app.route('/category', methods=['GET', 'POST'])
def get_all_category():
    if 'user_id' in session:
        db = DBwrapper()
        if request.method == 'GET':
            data = db.select('category',{'owner':(session['user_id'], 1)})
            return render_template("all_category.html", user_categories=data)
        else:
            category_name = request.form['category_name']
            category_owner = session['user_id']
            db.insert('category', {"name":category_name,"owner":category_owner})
            return redirect('/category')
    else:
        return redirect('/login')


@app.route('/category/<category_id>', methods=['GET', 'POST'])
def get_category(category_id):
    if 'user_id' in session:
        db = DBwrapper()
        if request.method == 'GET':
            transactions = db.select('transaction', {'category':category_id,'owner':session["user_id"]})
            current_category = db.select('category', {'id':category_id})
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
        db = DBwrapper()
        if request.method == 'GET':
            data = db.select('transaction', {'owner':session["user_id"], 'type':INCOME})

            return render_template("dashboard.html", transactions=data, dashboard_action='/income')
        else:
                transaction_description = request.form['description']
                transaction_category = request.form['category']
                transaction_amount = request.form['amount']
                transaction_date = request.form['date']
                transaction_owner = session['user_id']
                transaction_type = INCOME
                db.insert("transaction", {"description":transaction_description, "category":transaction_category, "amount":transaction_amount, "date":transaction_date, "owner":transaction_owner, "type":transaction_type})
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
        db = DBwrapper()
        if request.method == 'GET':
            data = db.select('transaction', {'owner': session["user_id"], 'type': INCOME})
            return render_template("dashboard.html", transactions=data, dashboard_action='/spend')
        else:
                transaction_description = request.form['description']
                transaction_category = request.form['category']
                transaction_amount = request.form['amount']
                transaction_date = request.form['date']
                transaction_owner = session['user_id']
                transaction_type = SPEND
                db.insert("transaction", {"description":transaction_description, "category":transaction_category, "amount":transaction_amount, "date":transaction_date, "owner":transaction_owner, "type":transaction_type})
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
