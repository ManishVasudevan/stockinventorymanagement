from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'manish123',
    'database': 'sims'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/')
def index():
    return render_template('stockcheck.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    item_code = request.form.get('itemCode')
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Query to fetch stock data based on item code
        query = """
            SELECT category, sub_category, material_description, 
                   COALESCE(good, 0) as good, 
                   COALESCE(damaged, 0) as damaged
            FROM stock 
            WHERE item_code = %s
        """
        cursor.execute(query, (item_code,))
        stock_data = cursor.fetchone()
        
        if stock_data:
            # Calculate total
            total = stock_data['good'] + stock_data['damaged']
            stock_data['total'] = total
            
            # Check if out of stock
            if total == 0:
                stock_data['out_of_stock'] = True
            else:
                stock_data['out_of_stock'] = False
                
            return jsonify(stock_data)
        else:
            return jsonify({'error': 'Item not found'}), 404
            
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)