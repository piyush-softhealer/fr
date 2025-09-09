from flask import Flask, send_file
import os
import main  # import your receipt generator

app = Flask(__name__)

@app.route("/")
def generate_receipt():
    data = main.generate_receipt_data()
    filename = f"receipt_{data['bill_no']}.png"
    path = main.render_receipt_to_image(data, out_path=filename)
    return send_file(path, mimetype="image/png", as_attachment=True, download_name=filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
