from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "manish123"
app.config["MYSQL_DB"] = "sims"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route("/")
def stock_entry():
    return render_template("stockentry.html")  # HTML file containing the provided form

@app.route("/update", methods=["POST"])
def update_stock():
    item_code = request.form.get("item_code")
    good = request.form.get("good", '0')
    damaged = request.form.get("damaged", '0')

    # Convert inputs to integers safely
    try:
        good = int(good) if good.strip() else 0
    except ValueError:
        good = 0

    try:
        damaged = int(damaged) if damaged.strip() else 0
    except ValueError:
        damaged = 0

    action = request.form.get("action")

    if not item_code or action not in ["add", "less"]:
        flash("Invalid input or action.")
        return redirect("/")

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT good, damaged FROM stock WHERE item_code = %s", [item_code])
    record = cursor.fetchone()

    if record:
        new_good = record["good"] + good if action == "add" else record["good"] - good
        new_damaged = record["damaged"] + damaged if action == "add" else record["damaged"] - damaged

        new_good = max(new_good, 0)
        new_damaged = max(new_damaged, 0)

        cursor.execute(
            "UPDATE stock SET good = %s, damaged = %s WHERE item_code = %s",
            (new_good, new_damaged, item_code),
        )
        mysql.connection.commit()
        flash(f"Stock updated for item {item_code}: Good - {new_good}, Damaged - {new_damaged}")
    else:
        flash(f"No record found for item code {item_code}")

    return redirect("/")

if __name__ == "__main__":
    app.secret_key = "abc123"
    app.run(debug=True)
