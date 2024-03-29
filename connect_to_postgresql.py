import psycopg2

def connect_to_postgresql():
    host = 'insideoutdatabaseserver.cja8kawgeoi3.ap-southeast-2.rds.amazonaws.com'
    port = 5432
    database = 'SampleDB'
    user = 'spandandb'
    password = 'dbpassword'

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None
    
def insert_user(username, hashedpassword, email):
    hashedpassword = hashedpassword
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            sql_insert = """INSERT INTO public."user"(username, password_hash, email) VALUES (%s, %s, %s)"""
            user_data = (username, hashedpassword, email)
            cursor.execute(sql_insert, user_data)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except psycopg2.Error as e: 
            print("Error inserting user:", e)
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    else:
        return False
    
def verify_user(username, hashedpassword):
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            sql_select = """SELECT id, username, password_hash FROM public."user" WHERE username = %s;"""
            user_data = (username,)
            cursor.execute(sql_select, user_data)
            user_data = cursor.fetchone()
            cursor.close()
            connection.close()
            if user_data:
                retrieved_id = user_data[0]
                retrieved_username = user_data[1]
                retrieved_password = user_data[2]
                if hashedpassword == retrieved_password:
                    print("Password matched")
                    return True, retrieved_id  # Return retrieved_id along with True
                else:
                    print("Password does not match")
                    return False, None
            else:
                print("User not found")
                return False, None
        except psycopg2.Error as e: 
            print("Error inserting user:", e)
            connection.rollback()
            cursor.close()
            connection.close()
            return False, None
        
def get_user_details(user_id):
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            sql_select = """SELECT id, username, email FROM public."user" WHERE id = %s;"""
            cursor.execute(sql_select, (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            connection.close()
            return user_data  # Returns user details as a tuple (id, username, email)
        except psycopg2.Error as e:
            print("Error fetching user details:", e)
            connection.rollback()
            cursor.close()
            connection.close()
            return None
    else:
        return None
    
def get_transaction_data(user_id):
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            sql_select = """SELECT * FROM public."transaction" WHERE user_id = %s;"""
            cursor.execute(sql_select, (user_id,))
            transaction_data = cursor.fetchall()
            print(transaction_data)
            cursor.close()
            connection.close()
            return transaction_data  # Returns user details as a tuple (id, username, email)
        except psycopg2.Error as e:
            print("Error fetching user details:", e)
            connection.rollback()
            cursor.close()
            connection.close()
            return None
    else:
        return None
    
def add_transaction_data(amount, date, category, description, userid, stateid):
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            sql_insert = """INSERT INTO public."transaction" (amount, date, category, description, user_id, state_id) VALUES (%s, %s, %s, %s, %s, %s)"""
            debit_data = (amount, date, category, description, userid, stateid)
            cursor.execute(sql_insert, debit_data)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except psycopg2.Error as e: 
            print("Error inserting transaction:", e)
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    else:
        return False
    
def total_expenses(user_id):
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            sql_select = """SELECT SUM(amount) AS total_amount FROM public."transaction" WHERE user_id = %s AND state_id = 1"""
            cursor.execute(sql_select, (user_id,))
            total_expenses_data = cursor.fetchone()
            cursor.close()
            connection.close()
            return total_expenses_data
        except psycopg2.Error as e: 
            print("Error Fetching data:", e)
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    else:
        return False
    
def total_income(user_id):
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            sql_select = """SELECT SUM(amount) AS total_amount FROM public."transaction" WHERE user_id = %s AND state_id IN (2, 3);"""
            cursor.execute(sql_select, (user_id,))
            total_income_data = cursor.fetchone()
            cursor.close()
            connection.close()
            return total_income_data
        except psycopg2.Error as e: 
            print("Error Fetching data:", e)
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    else:
        return False
    
def total_investments(user_id):
    connection = connect_to_postgresql()
    if connection:
        try:
            cursor = connection.cursor()
            sql_select = """SELECT SUM(amount) AS total_amount FROM public."transaction" WHERE user_id = %s AND state_id = 3"""
            cursor.execute(sql_select, (user_id,))
            total_investments_data = cursor.fetchone()
            cursor.close()
            connection.close()
            return total_investments_data
        except psycopg2.Error as e: 
            print("Error Fetching data:", e)
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    else:
        return False