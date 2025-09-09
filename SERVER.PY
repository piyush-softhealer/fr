from flask import Flask, send_file
from main import generate_receipt_data, render_receipt_to_image
import os

app = Flask(__name__)

@app.route("/")
def home():
    data = generate_receipt_data()
    path = render_receipt_to_image(data, out_path="receipt.png")
    return send_file(path, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
