# SERVER.PY - Flask Application
from flask import Flask, send_file, render_template_string
import main
import os

app = Flask(__name__)

@app.route("/")
def generate_receipt():
    data = main.generate_receipt_data()
    filename = f"receipt_{data['bill_no']}.jpg"
    path, data = main.generate_ultra_realistic_receipt(out_path=filename)

    # HTML template to display the receipt (using f-string only)
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Realistic Receipt Generator</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; text-align: center; background-color: #f5f5f5; }}
        h1 {{ color: #2c3e50; }}
        .receipt-container {{ margin: 20px auto; max-width: 500px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px; }}
        button {{ background-color: #3498db; color: white; border: none; padding: 12px 24px; 
                 border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px; }}
        button:hover {{ background-color: #2980b9; }}
        .info {{ margin: 15px 0; color: #555; }}
    </style>
</head>
<body>
    <h1>Realistic Receipt Generator</h1>
    <p>Click the button to generate a new receipt:</p>
    <button onclick="window.location.reload()">Generate New Receipt</button>
    
    <div class="receipt-container">
        <div class="info">Bill No: {data['bill_no']} | Date: {data['date']}</div>
        <img src="/receipt_image" alt="Generated Receipt">
    </div>
    
    <p>Each receipt is randomly generated with realistic Indian data.</p>
</body>
</html>
"""

    return render_template_string(html_template)

@app.route("/receipt_image")
def receipt_image():
    # Generate a new receipt for the image endpoint
    data = main.generate_receipt_data()
    filename = "temp_receipt.jpg"
    path, data = main.generate_ultra_realistic_receipt(out_path=filename)

    return send_file(filename, mimetype="image/jpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
