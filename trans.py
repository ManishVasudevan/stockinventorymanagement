from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using flash messages

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "manish123"
app.config["MYSQL_DB"] = "sims"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Loading Home Page
@app.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inventory_transactions")
    res = cur.fetchall()
    cur.close()
    return render_template("transactions.html", datas=res)

# Add Transaction
@app.route("/save_transaction_data", methods=['POST'])
def addTransactions():
    if request.method == 'POST':
        date = request.form['date']
        transactionsid = request.form['transaction-no']
        stocktransactions = request.form['stock-transactions']
        distributorname = request.form['distributor-name']
        location = request.form['location']
        transportname = request.form['transport-name']
        vehiclenumber = request.form['vehicle-number']
        stocktype = request.form['stock_type']
        itemCode = request.form['itemCode']
        category = request.form['category']
        subCategory = request.form['subCategory']
        materialDescription = request.form['materialDescription']
        quantity = request.form['quantity']
        price = request.form['price']
        gross = request.form['gross']
        condition = request.form['condition']
        remarks = request.form['remarks']

        cur = mysql.connection.cursor()
        cur.execute("""
        INSERT INTO inventory_transactions (
        DATE, TRANSACTIONS_ID, STOCK_TRANSACTIONS, DISTRIBUTOR_NAME, 
        LOCATION, TRANSPORT_NAME, VEHICLE_NUMBER, STOCK_TYPE, 
        ITEM_CODE, CATEGORY, SUB_CATEGORY, MATERIAL_DESCRIPTION, 
        QUANTITY, PRICE, GROSS, `CONDITION`, REMARKS
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
        date, transactionsid, stocktransactions, distributorname, location, 
        transportname, vehiclenumber, stocktype, itemCode, category, 
        subCategory, materialDescription, quantity, price, gross, 
        condition, remarks
        ))

        mysql.connection.commit()
        cur.close()
        flash('Transaction Details Added')
        return redirect(url_for("home"))

# Ensure the script runs when executed directly
if __name__ == "__main__":
    app.run(debug=True)
