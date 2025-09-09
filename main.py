#!/usr/bin/env python3
# Flask Receipt Generator - with 100+ products and random realistic data

import random
import datetime
import os
from flask import Flask, send_file, render_template_string
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# 100+ product names with realistic base prices (in ₹)
products = [
    ("Apple", 80), ("Banana", 40), ("Grapes", 120), ("Orange", 60), ("Papaya", 30), 
    ("Mango", 100), ("Pineapple", 50), ("Kiwi", 70), ("Pear", 90), ("Guava", 35),
    ("Strawberry", 150), ("Blueberry", 200), ("Watermelon", 25), ("Pomegranate", 110),
    ("Cherry", 180), ("Peach", 85), ("Plum", 75), ("Apricot", 95), ("Lemon", 20),
    ("Coconut", 30), ("Dragon Fruit", 160), ("Lychee", 140), ("Fig", 130), 
    ("Custard Apple", 90), ("Jackfruit", 60), ("Dates", 220), ("Blackberry", 190),
    ("Raspberry", 210), ("Sapota", 45), ("Muskmelon", 35), ("Tangerine", 65),
    ("Starfruit", 120), ("Passion Fruit", 170), ("Durian", 250), ("Longan", 110),
    ("Mulberry", 160), ("Cranberry", 180), ("Olive", 140), ("Tomato", 25),
    ("Potato", 20), ("Onion", 30), ("Garlic", 150), ("Carrot", 40), ("Beetroot", 35),
    ("Radish", 25), ("Spinach", 20), ("Cabbage", 25), ("Cauliflower", 30),
    ("Broccoli", 60), ("Pumpkin", 35), ("Bottle Gourd", 30), ("Bitter Gourd", 40),
    ("Ladyfinger", 50), ("Beans", 60), ("Peas", 70), ("Corn", 25), ("Ginger", 100),
    ("Chili", 80), ("Cucumber", 30), ("Zucchini", 50), ("Capsicum", 60),
    ("Brinjal", 40), ("Mushroom", 90), ("Lettuce", 50), ("Celery", 40),
    ("Spring Onion", 30), ("Coriander", 20), ("Mint", 25), ("Basil", 100),
    ("Thyme", 120), ("Rosemary", 130), ("Sage", 110), ("Parsley", 40), ("Leek", 50),
    ("Kale", 60), ("Fenugreek", 30), ("Drumstick", 40), ("Turnip", 35),
    ("Sweet Potato", 45), ("Yam", 50), ("Arbi", 40), ("Colocasia", 35),
    ("Mustard Greens", 25), ("Amaranthus", 20), ("Okra", 55), ("Pumpkin Seeds", 180),
    ("Sunflower Seeds", 160), ("Almonds", 500), ("Cashew", 600), ("Walnut", 450),
    ("Pistachio", 700), ("Groundnut", 120), ("Raisin", 200), ("Clove", 400),
    ("Cardamom", 800), ("Cinnamon", 300), ("Black Pepper", 350), ("Turmeric", 150),
    ("Fennel", 200), ("Ajwain", 250), ("Fenugreek Seeds", 180), ("Jaggery", 100)
]

company_prefixes = [
    "Fresh", "Green", "Daily", "Urban", "Organic", "Prime", "Budget",
    "Harvest", "Royal", "Metro", "Super", "Mega", "Family", "City",
    "Friendly", "Quick", "Value", "Best", "Smart", "Local", "Natural"
]

company_suffixes = [
    "Mart", "Grocery", "Store", "Bazaar", "Grocers", "Market",
    "Provision", "Center", "Corner", "Depot", "Shop", "Supermarket",
    "Foods", "Freshmart", "Veggies", "Fruits", "Minimart"
]

places = [
    "Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Nagpur", "Surat",
    "Bhopal", "Indore", "Patna", "Vadodara", "Ghaziabad", "Ludhiana",
    "Agra", "Varanasi", "Mysuru", "Coimbatore", "Thiruvananthapuram",
    "Rajkot", "Nashik", "Kanpur", "Noida", "Amritsar", "Guwahati", "Ranchi"
]

streets = [
    "MG Road", "Station Road", "1st Main", "Park Street", "Church Lane",
    "Market Lane", "Rose Ave", "Victoria St.", "Baker Street", "Gandhi Road",
    "Nehru Marg", "Tilak Road", "Jawahar Nagar", "Rajpur Road", "Civil Lines",
    "LBS Marg", "Link Road", "Anna Salai", "BTM Layout", "Jayanagar",
    "Charminar Road", "Salt Lake Sector V", "Dak Bunglow", "Ring Road"
]

# Indian first names for cashiers
first_names = [
    "Ravi", "Asha", "Sunil", "Neha", "Rohit", "Priya", "Ankit", "Sneha",
    "Amit", "Kavita", "Raj", "Pooja", "Vikram", "Divya", "Sanjay", "Meera",
    "Arun", "Anjali", "Mohan", "Sarika", "Vijay", "Swati", "Nitin", "Kiran"
]

# Indian last names for cashiers
last_names = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Mehta", "Reddy", "Rao",
    "Verma", "Malhotra", "Jain", "Shah", "Pandey", "Yadav", "Mishra", "Chauhan"
]

def random_gstin():
    state = f"{random.randint(1,35):02d}"
    pan = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + \
          ''.join(random.choices("0123456789", k=4)) + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    entity = random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return state + pan + entity + "Z" + random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def generate_receipt_data():
    num_items = random.randint(3, 10)
    items = []
    for _ in range(num_items):
        product, base_price = random.choice(products)
        desc_options = ["(1kg)", "(Dozen)", "(500g)", "(250g)", "(per piece)", "(bunch)", "(pack)"]
        desc = random.choice(desc_options)
        qty = random.randint(1, 5)
        
        # Add some price variation (±20%)
        variation = random.uniform(0.8, 1.2)
        rate = int(base_price * variation)
        
        amount = qty * rate
        items.append((qty, f"{product} {desc}", rate, amount))
    
    company = f"{random.choice(company_prefixes)} {random.choice(company_suffixes)}"
    gstin = random_gstin()
    phone = f"+91-{random.randint(60000, 99999)}{random.randint(10000, 99999)}"
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    time = datetime.datetime.now().strftime("%I:%M %p")
    cashier = f"{random.choice(first_names)} {random.choice(last_names)}"
    bill_no = f"{random.randint(1000, 9999):04d}"
    place = random.choice(places)
    address = f"{random.randint(10, 999)} {random.choice(streets)}, {place} - {random.randint(400001, 799999)}"
    
    subtotal = sum(a for (_, _, _, a) in items)
    gst = int(round(subtotal * 0.05))
    total = subtotal + gst
    
    discount = 0
    if random.random() < 0.3:  # 30% chance
        discount = int(round(subtotal * random.uniform(0.05, 0.15)))
        total = subtotal + gst - discount
    
    return {
        "company": company,
        "gstin": gstin,
        "phone": phone,
        "date": date,
        "time": time,
        "cashier": cashier,
        "bill_no": bill_no,
        "address": address,
        "items": items,
        "subtotal": subtotal,
        "gst": gst,
        "discount": discount,
        "total": total
    }

def render_receipt_to_image(data, out_path="receipt.png", width=400):
    line_height = 20
    padding = 20
    height = padding * 2 + 400 + len(data["items"]) * (line_height + 6)
    img = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(img)
    
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        ]
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 14)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    x, y = padding, padding
    def draw_line(s="", align="left"):
        nonlocal y
        if align == "center":
            text_width = draw.textlength(s, font=font)
            draw.text(((width - text_width) / 2, y), s, font=font, fill=0)
        elif align == "right":
            text_width = draw.textlength(s, font=font)
            draw.text((width - padding - text_width, y), s, font=font, fill=0)
        else:
            draw.text((x, y), s, font=font, fill=0)
        y += line_height
    
    # HEADER
    draw_line(data["company"].upper(), "center")
    draw_line(data["address"], "center")
    draw_line(f"Phone: {data['phone']}", "center")
    draw_line(f"GSTIN: {data['gstin']}", "center")
    draw_line("-" * 40)
    
    draw_line(f"Bill No: {data['bill_no']}")
    draw_line(f"Date: {data['date']}   Time: {data['time']}")
    draw_line(f"Cashier: {data['cashier']}")
    draw_line("-" * 40)
    
    draw_line("Qty  Item                Rate  Amount")
    draw_line("-" * 40)
    for qty, name, rate, amount in data["items"]:
        if len(name) > 18: name = name[:15] + "..."
        line = f"{qty:<4} {name:<19} {rate:>4}  {amount:>5}"
        draw_line(line)
    draw_line("-" * 40)
    
    draw_line(f"Subtotal: {data['subtotal']:>28}")
    draw_line(f"GST (5%): {data['gst']:>28}")
    if data['discount'] > 0:
        draw_line(f"Discount: -{data['discount']:>26}")
    draw_line("-" * 40)
    draw_line(f"TOTAL: {data['total']:>30}")
    draw_line("-" * 40)
    draw_line("Thank you for shopping!", "center")
    draw_line("Please visit again!", "center")
    
    img.save(out_path)
    return out_path

@app.route("/")
def home():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Receipt Generator</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
            h1 { color: #2c3e50; }
            .receipt { margin: 20px auto; max-width: 500px; border: 1px solid #ddd; padding: 20px; }
            img { max-width: 100%; height: auto; border: 1px solid #eee; }
            button { background-color: #3498db; color: white; border: none; padding: 10px 20px; 
                     border-radius: 4px; cursor: pointer; font-size: 16px; }
            button:hover { background-color: #2980b9; }
        </style>
    </head>
    <body>
        <h1>Receipt Generator</h1>
        <p>Click the button to generate a new receipt:</p>
        <button onclick="window.location.reload()">Generate New Receipt</button>
        <div class="receipt">
            <img src="/receipt.png" alt="Generated Receipt">
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route("/receipt.png")
def receipt_image():
    data = generate_receipt_data()
    filename = f"receipt_{data['bill_no']}.png"
    path = render_receipt_to_image(data, out_path=filename)
    return send_file(path, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)