from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configure SQL Server connection
app.config['DATABASE_CONNECTION_STRING'] = 'DRIVER={ODBC Driver 17 for SQL ' \
                                           'Server};SERVER=CNIL-BDJP063;DATABASE=Warrior;UID=sa;PWD=abcd@1234'


@app.route('/')
def index():
    return render_template('HomePage.html')


# Define a route for a specific URL
@app.route('/CustomerPOS', methods=['GET', 'POST'])
def customer_interaction():
    if request.method == 'POST':
        try:
            mob_number = request.form['mobile1']
            bill_number = request.form['bill1']
            cname = request.form['Name']
            amount = request.form['amount1']
            status = 'N'

            # Connect to SQL Server
            conn = pyodbc.connect(app.config['DATABASE_CONNECTION_STRING'])
            cursor = conn.cursor()

            # Insert data into the database
            cursor.execute('INSERT INTO CustomerDetails (CName, mobile, bill, Amount, Status) VALUES (?, ?, ?, ?, ?)',
                           (cname, mob_number, bill_number, amount, status))
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            # Show a popup dialog box using JavaScript
            return '''
                <script>
                    alert('Customer Saved successfully');
                    window.location.href = '/CustomerPOS';
                </script>
            '''
        except Exception as e:
            return f'Error placing order: {str(e)}'

    return render_template('customer_interaction.html')


# Define a route with dynamic URL parameters
@app.route('/Dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        return redirect(url_for('search_customer'))
    return render_template('dashboard.html')


@app.route('/search_customer', methods=['POST'])
def search_customer():
    search_param = request.form['search_param']
    search_value = request.form['search_value']

    try:
        # Connect to SQL Server
        conn = pyodbc.connect(app.config['DATABASE_CONNECTION_STRING'])
        cursor = conn.cursor()

        # Execute SQL query to search for customers
        query = f"SELECT * FROM CustomerDetails WHERE {search_param} LIKE ?"
        cursor.execute(query, ('%' + search_value + '%',))
        customers = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        return render_template('dashboard.html', customers=customers)
    except Exception as e:
        return f'Error searching customers: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True)
