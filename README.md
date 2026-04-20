# Experiment 11 (23BIS70027) – Microservices-Based Backend Module

## Objective
To develop a **microservices-based backend system** using Flask, where:
- One service handles **Customer data**
- Another service handles **Order data**
- Services communicate using **HTTP requests**

## Project Structure

```
Experiment11/
│
├── customer-service/
│   ├── app.py
│   ├── requirements.txt
│   
│
├── order-service/
│   ├── app.py
│   ├── requirements.txt
│   
│
├── screenshots/
│   ├── 1_CUSTOMERSERVER.png
│   ├── 2_ORDERSERVER.png
│   ├── 3_TESTALL.png
│   ├── 4_UPDATE.png
|   ├── 5_VERIFY.png
│   ├── 6_MAINTESTCUSTSERVICE.png
│   └── 7_ERRORCASE.png
│
└── README.md   ← (MAIN project README)
```

## ⚙️ Technologies Used
- Python (Flask)
- Requests Library
- Postman (API Testing)
- Render (Deployment)

## Microservices Overview

### 1. Customer Service

- Stores customer data (in-memory)
- Fetches customer details
- Calls Order Service to retrieve orders

**Endpoint:** GET /customers/<user_id>/orders

### 2. Order Service

- Stores order data (in-memory)
- Retrieves orders for a user
- Updates order status

**Endpoints:**
- GET /orders/user/<user_id>
- PUT /orders/<order_id>/status

## Source Code

### Customer Service (`customer_app.py`)

```python
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Dummy customer data
customers = {
    1: {"name": "John", "orders": [101, 102]},
    2: {"name": "Alice", "orders": [103]}
}

# 🔴 IMPORTANT: Change this AFTER deploying Order Service on Render
ORDER_SERVICE_URL = os.environ.get(
    "ORDER_SERVICE_URL",
    "http://127.0.0.1:5001/orders"  # Local fallback
)

# ✅ Home route
@app.route('/')
def home():
    return "Customer Service is running 🚀"

# ✅ Main API
@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    customer = customers.get(customer_id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        response = requests.get(ORDER_SERVICE_URL, timeout=5)
        response.raise_for_status()
        all_orders = response.json()

        customer_orders = [
            order for order in all_orders
            if order.get("id") in customer["orders"]
        ]

        return jsonify({
            "customer": customer["name"],
            "orders": customer_orders
        })

    except requests.exceptions.RequestException:
        return jsonify({"error": "Order service unavailable"}), 500


# ✅ Render-compatible run
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
```

---

### Order Service (`order_app.py`)

```python
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Dummy order data
orders = [
    {"id": 101, "item": "Laptop", "status": "Pending"},
    {"id": 102, "item": "Phone", "status": "Shipped"},
    {"id": 103, "item": "Tablet", "status": "Delivered"}
]

# ✅ Home route
@app.route('/')
def home():
    return "Order Service is running 🚀"

# ✅ Get all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

# ✅ Update order
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    if "status" not in data:
        return jsonify({"error": "Missing 'status' field"}), 400

    for order in orders:
        if order["id"] == order_id:
            order["status"] = data["status"]
            return jsonify({
                "message": "Order updated successfully",
                "order": order
            }), 200

    return jsonify({"error": "Order not found"}), 404


# ✅ Render-compatible run
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
```

---

## Deployment Links

- Customer Service: https://two3bis70027-experiment11.onrender.com
- Order Service:    https://two3bis70027-experiment11-orderservice.onrender.com

## Working Flow

1. Client sends request:

   ```
   /customers/101/orders
   ```
2. Customer Service fetches customer data
3. Calls Order Service API
4. Combines response and returns JSON


## Learning Outcomes
* Understood Microservices Architecture
* Implemented Service-to-Service Communication
* Built REST APIs using Flask
* Learned GET and PUT methods
* Worked with in-memory data storage
* Deployed services using Render
* Tested APIs using Postman
* Learned error handling in APIs