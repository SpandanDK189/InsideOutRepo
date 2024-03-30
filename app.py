import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session
from connect_to_postgresql import insert_user, verify_user, connect_to_postgresql, get_user_details, get_transaction_data, add_transaction_data, total_expenses, total_income, total_investments
import functions

app = Flask(__name__)
app.secret_key = '7a3b46a30396e2e12ce95ecc5076a0e600bfa0b9b73ba7f5ba0f470f85ff088e'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("request is made")
        if 'submitbutton' in request.form:
            submitbutton = request.form['submitbutton']
            if submitbutton == 'login':
                username = request.form['username']
                password = request.form['password']
                hashedpassword = functions.hashFunction(password)
                success, retrieved_id = verify_user(username, hashedpassword)  # Capture the returned values
                if success:
                    session['user_id'] = retrieved_id  # Store retrieved_id in session
                    return redirect(url_for('dashboard'))
                else:
                    session['message'] = 'Invalid credentials. Please try again.'
                    return redirect(url_for('index'))
            
            elif submitbutton == 'signup':
                username = request.form['new-username']
                password = request.form['new-password']
                email = request.form['new-email']
                hashedpassword = functions.hashFunction(password)
                flag = insert_user(username, hashedpassword, email)
                if flag:
                    message = 'Signup successful. Please login.'
                    return render_template('index.html')    
    return render_template('index.html', message=session.pop('message', None))

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user_data = get_user_details(user_id)
        transaction_data = get_transaction_data(user_id)

        totalexpenses = total_expenses(user_id)
        totalexpenses = totalexpenses[0]

        totalincome = total_income(user_id)
        totalincome = totalincome[0]

        totalinvestments = total_investments(user_id)
        totalinvestments = totalinvestments[0]

        if user_data:
            return render_template('dashboard.html', user_data=user_data, transaction_data=transaction_data, totalexpenses = totalexpenses, totalincome = totalincome, totalinvestments = totalinvestments)
        else:
            return render_template(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_options():
    if request.method == 'POST':
        option = request.form['options']
        update_option_in_database(option)
        return redirect(url_for('dashboard'))

@app.route('/forms', methods=['GET', 'POST'])
def show_forms():
    user_id = session.get('user_id')
    if user_id:
        user_data = get_user_details(user_id)
    if user_data:
        if request.method == 'POST':
            if 'addButton' in request.form:
                return render_template('forms.html', user_data=user_data)
            
@app.route('/debit', methods=['GET', 'POST'])
def debit_forms():
    if request.method == 'POST':
        print("request is made for debit")
        if 'debitButton' in request.form:
            debitButton = request.form['debitButton']
            if debitButton == debitButton:
                amount = request.form['expenses-amount']
                date = request.form['expenses-date']
                category = request.form['expenses-category']
                description = request.form['expenses-description']
                userid = request.form['user-id']
                stateid = request.form['state-id']
                flag = add_transaction_data(amount, date, category, description, userid, stateid)
                if flag:
                    return redirect(url_for('dashboard'))
                
@app.route('/credit', methods=['GET', 'POST'])
def credit_forms():
    if request.method == 'POST':
        print("request is made for credit")
        if 'creditButton' in request.form:
            creditButton = request.form['creditButton']
            if creditButton == creditButton:
                amount = request.form['income-amount']
                date = request.form['income-date']
                category = request.form['income-category']
                description = request.form['income-description']
                userid = request.form['user-id']
                stateid = request.form['state-id']
                flag = add_transaction_data(amount, date, category, description, userid, stateid)
                if flag:
                    return redirect(url_for('dashboard'))

@app.route('/investment', methods=['GET', 'POST'])
def investments_forms():
    if request.method == 'POST':
        print("request is made for investment")
        if 'investmentButton' in request.form:
            investmentButton = request.form['investmentButton']
            if investmentButton == investmentButton:
                amount = request.form['investments-amount']
                date = request.form['investments-date']
                category = request.form['investments-type']
                description = request.form['investments-description']
                userid = request.form['user-id']
                stateid = request.form['state-id']
                flag = add_transaction_data(amount, date, category, description, userid, stateid)
                if flag:
                    return redirect(url_for('dashboard'))

def update_option_in_database(option):
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            # Assuming you have a table named 'options' with a column 'selected_option'
            sql_update = "UPDATE options SET selected_option = %s WHERE id = 1;"  # Assuming ID 1 for simplicity
            cursor.execute(sql_update, (option,))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print("Error updating option:", e)
            connection.rollback()
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
