from flask import Flask, render_template, request, url_for, flash,request, jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'M@tech@pp1234'
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)



app = Flask(__name__)

# In-memory storage for customers and orders
customers = []
orders = []

# Admin login
@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    if data["username"] == "admin" and data["password"] == "admin123":
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# Create a customer profile
@app.route("/admin/customers", methods=["POST"])
def create_customer():
    data = request.get_json()
    customer = {"id": len(customers) + 1, "name": data["name"], "email": data["email"], "phone": data["phone"], "active": True}
    customers.append(customer)
    return jsonify({"message": "Customer created successfully"})

# Retrieve all customers
@app.route("/admin/customers", methods=["GET"])
def get_all_customers():
    return jsonify(customers)

# Retrieve a specific customer by ID
@app.route("/admin/customers/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer = next((customer for customer in customers if customer["id"] == customer_id), None)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404
    return jsonify(customer)

# Update a customer profile
@app.route("/admin/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = next((customer for customer in customers if customer["id"] == customer_id), None)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404
    data = request.get_json()
    customer["name"] = data["name"]
    customer["email"] = data["email"]
    customer["phone"] = data["phone"]
    customer["active"] = data["active"]
    return jsonify({"message": "Customer updated successfully"})

# Deactivate a customer profile
@app.route("/admin/customers/<int:customer_id>/deactivate", methods=["PUT"])
def deactivate_customer(customer_id):
    customer = next((customer for customer in customers if customer["id"] == customer_id), None)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404
    customer["active"] = False
    return jsonify({"message": "Customer deactivated successfully"})

# Approve a customer order
@app.route("/admin/orders/<int:order_id>/approve", methods=["PUT"])
def approve_order(order_id):
    order = next((order for order in orders if order["id"] == order_id), None)
    if order is None:
        return jsonify({"message": "Order not found"}), 404
    order["status"] = "Approved"
    return jsonify({"message": "Order approved successfully"})

# Mark a customer order as fulfilled
@app.route("/admin/orders/<int:order_id>/fulfill", methods=["PUT"])
def fulfill_order(order_id):
    order = next((order for order in orders if order["id"] == order_id), None)
    if order is None:
        return jsonify({"message": "Order not found"}), 404
    order["status"] = "Fulfilled"
    return jsonify({"message": "Order fulfilled successfully"})

# Customer signup
@app.route("/customers/signup", methods=["POST"])
def customer_signup():
    data = request.get_json()
    customer = {"id": len(customers) + 1, "name": data["name"], "email": data["email"], "password": data["password"]}
    customers.append(customer)
    return jsonify({"message": "Signup successful"})

@app.route("/customers/login", methods=["POST"])
def customer_login():
    data = request.get_json()
    customer = next((customer for customer in customers if customer["email"] == data["email"]), None)
    if customer is None or customer["password"] != data["password"]:
        return jsonify({"message": "Invalid email or password"}), 401
    return jsonify({"message": "Login successful"})
@app.route("/customers/furniture", methods=["GET"])
def get_furniture_catalog():
# Implement your logic to retrieve furniture catalog
    furniture = [{"id": 1, "name": "Sofa", "price": 100},
    {"id": 2, "name": "Chair", "price": 50},
    {"id": 3, "name": "Table", "price": 150}]
    return jsonify(furniture)

@app.route("/customers/orders", methods=["POST"])
def place_order():
    data = request.get_json()
    customer = next((customer for customer in customers if customer["email"] == data["email"]), None)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404
    order_items = []
    for item in data["items"]:
        furniture = next((furniture for furniture in get_furniture_catalog() if furniture["id"] == item["furniture_id"]), None)
        if furniture is None:
            return jsonify({"message": "Furniture not found"}), 404
    order_items.append({"furniture": furniture["name"], "quantity": item["quantity"], "price": furniture["price"]})
    order = {"id": len(orders) + 1, "customer_id": customer["id"], "items": order_items, "status": "Pending"}
    orders.append(order)
    return jsonify({"message": "Order placed successfully"})

@app.route("/customers/orders/int:order_id/cancel", methods=["PUT"])
def cancel_order(order_id):
    order = next((order for order in orders if order["id"] == order_id), None)
    if order is None:
        return jsonify({"message": "Order not found"}), 404
    if order["status"] == "Approved":
        return jsonify({"message": "Cannot cancel an approved order"}), 400
    order["status"] = "Cancelled"
    return jsonify({"message": "Order cancelled successfully"})

if __name__ == "__main__":
    app.run(debug=True)
