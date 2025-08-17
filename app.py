from flask import Flask, request, render_template, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key =  'qw<ert?yu111io2p"2a3s>.>4d5fghjkl'
INCOME = 1
SPEND = 2


class DatabaseManager():
    def __init__(self, database_name):
        self.database_name = database_name
    def __enter__(self):
        self.connect = sqlite3.connect(self.database_name)
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

@app.route('/login', methods=['GET','POST'])
def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        password = request.form['password']
        email = request.form['email']
        with DatabaseManager('financial_tracker.db') as cursor:
            res = cursor.execute(f'SELECT id FROM user WHERE email = "{email}" AND password = "{password}"')
            data = res.fetchone()
        if data:
            session['user_id'] = data[0]
            return f'You are in {email} {password}'
        else:
            return f'Wrong password'



@app.route('/register', methods=['GET','POST'])
def get_register():

    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        with DatabaseManager('financial_tracker.db') as cursor:
            cursor.execute('INSERT INTO user (name,surname, password, email) VALUES (?,?,?,?)',(username,surname,password,email))

        return f'User registered: {username} {password} {email} {surname}'

@app.route('/category', methods=['GET', 'POST'])
def get_all_category():
    if request.method == 'GET':
        return 'hello world GET'
    else:
        return 'hello world POST'

@app.route('/category/<category_id>', methods=['GET', 'POST'])
def get_category(category_id):
    if request.method == 'GET':
        return render_template('one_category.html')
    else:
        return 'edit category'

@app.route('/category/<category_id>/delete', methods=['GET'])
def delete_category(category_id):
    return f"hello world DELETE {category_id}"


@app.route('/income', methods=['GET', 'POST'])
def get_all_income():
    if 'user_id' in session:
        if request.method == 'GET':
            with DatabaseManager('financial_tracker.db') as cursor:
                print(session['user_id'],'======', session)
                res = cursor.execute('SELECT * FROM "transaction" WHERE owner = ? AND type = ?', ((session["user_id"]), INCOME))
                data = res.fetchall()
            return render_template("dashboard.html", transactions=data, dashboard_action='/income')
        else:
            with DatabaseManager('financial_tracker.db') as cursor:
                transaction_description = request.form['description']
                transaction_category = request.form['category']
                transaction_amount = request.form['amount']
                transaction_date = request.form['date']
                transaction_owner = session['user_id']
                transaction_type = INCOME
                cursor.execute('INSERT INTO "transcation" (description, category, amount, date, owner, type) VALUES (?,?,?,?,?,?)',
                               (transaction_description, transaction_category, transaction_amount, transaction_date, transaction_owner, transaction_type))
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
        if request.method == 'GET':
            with DatabaseManager('financial_tracker.db') as cursor:
                print(session['user_id'], '======', session)
                res = cursor.execute('SELECT * FROM "transaction" WHERE owner = ? AND type = ?',
                                     ((session["user_id"]), SPEND))
                data = res.fetchall()
            return render_template("dashboard.html", transactions=data, dashboard_action='/spend')
        else:
            with DatabaseManager('financial_tracker.db') as cursor:
                transaction_description = request.form['description']
                transaction_category = request.form['category']
                transaction_amount = request.form['amount']
                transaction_date = request.form['date']
                transaction_owner = session['user_id']
                transaction_type = SPEND
                cursor.execute('INSERT INTO "transcation" (description, category, amount, date, owner, type) VALUES (?,?,?,?,?,?)',
                             (transaction_description, transaction_category, transaction_amount, transaction_date,
                     transaction_owner, transaction_type))
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