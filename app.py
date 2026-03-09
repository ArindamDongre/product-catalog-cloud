from flask import Flask, request, render_template, redirect
import sqlite3
import os

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("products.db")
    conn.row_factory = sqlite3.Row

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()

    return conn

@app.route("/")
def index():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route("/add", methods=["GET","POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        if name.strip() == "" or price.strip() == "":
            return "Invalid input! Name and price required."

        conn = get_db()
        conn.execute(
            "INSERT INTO products (name, price) VALUES (?, ?)",
            (name, price)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_product.html")

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)