from flask import Flask, request, render_template

app = Flask(__name__)

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
        username = request.form['username']
        password = request.form['password']
        return f'hello world POST {username} {password}'

@app.route('/register', methods=['GET','POST'])
def get_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        return f'hello world POST {username} {password}'

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
    if request.method == 'GET':
        return 'hello world GET'
    else:
        return 'hello world POST'

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
    if request.method == 'GET':
        return 'hello world GET'
    else:
        return 'hello world POST'

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