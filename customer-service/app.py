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