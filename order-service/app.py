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