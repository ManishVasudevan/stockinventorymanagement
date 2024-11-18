import os
from flask import Flask, render_template, request, send_file
import mysql.connector
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# MySQL Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'manish123',
    'database': 'sims'
}

# Function to create database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return connection

# Route for rendering the report form
@app.route('/')
def index():
    return render_template('Report.html')

# Route to handle form submission and export data to Excel
@app.route('/export', methods=['POST'])
def export_report():
    start_date = request.form.get('start-date')
    end_date = request.form.get('end-date')
    report_type = request.form.get('stock_transactions')

    # Initialize query
    query = ""
    if report_type == "incoming":
        # Transactions report query with date range
        if start_date and end_date:
            query = f"SELECT * FROM inventory_transactions WHERE date BETWEEN '{start_date}' AND '{end_date}'"
        else:
            return "Start Date and End Date are required for Transactions Report"
    
    elif report_type == "outgoing":
        # Stock report query (no date range)
        query = "SELECT * FROM stock"

    # If query is still empty, return error
    if not query:
        return "Invalid report type selected."

    # Fetch data from database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()

    if not data:
        return "No data found for the given parameters."

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)

    # Generate an Excel file
    file_name = "report.xlsx"
    df.to_excel(file_name, index=False, engine='openpyxl')

    # Send the file as a download
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)