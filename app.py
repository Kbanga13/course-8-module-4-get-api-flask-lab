from flask import Flask, jsonify, request
from data import products

app = Flask(__name__)


# Homepage: returns a simple welcome message as JSON so clients can confirm
# the API is reachable.
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Product Catalog API"})


# GET /products
#   - No query string: returns the full product list.
#   - ?category=<value>: returns only products in that category.
# Category comparison is case-insensitive so "Books" and "books" both match.
@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get("category")
    if category:
        filtered = [
            p for p in products if p["category"].lower() == category.lower()
        ]
        return jsonify(filtered)
    return jsonify(products)


# GET /products/<id>
# <int:id> restricts the path to integers, so non-numeric IDs 404 automatically.
# If no product matches, return a JSON error with a 404 status code.
@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    product = next((p for p in products if p["id"] == id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


if __name__ == "__main__":
    app.run(debug=True)
