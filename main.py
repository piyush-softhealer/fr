# main.py - Receipt Generation Functions
import random
import datetime
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

# Product database with realistic prices (in ₹)
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
    ("Mumbai", "MH"), ("Delhi", "DL"), ("Bengaluru", "KA"), ("Chennai", "TN"), ("Hyderabad", "TS"), ("Kolkata", "WB"),
    ("Pune", "MH"), ("Ahmedabad", "GJ"), ("Jaipur", "RJ"), ("Lucknow", "UP"), ("Nagpur", "MH"), ("Surat", "GJ"),
    ("Bhopal", "MP"), ("Indore", "MP"), ("Patna", "BR"), ("Vadodara", "GJ"), ("Ghaziabad", "UP"), ("Ludhiana", "PB"),
    ("Agra", "UP"), ("Varanasi", "UP"), ("Mysuru", "KA"), ("Coimbatore", "TN"), 
    ("Thiruvananthapuram", "KL"), ("Rajkot", "GJ"), ("Nashik", "MH"), ("Kanpur", "UP"), 
    ("Noida", "UP"), ("Amritsar", "PB"), ("Guwahati", "AS"), ("Ranchi", "JH")
]

streets = [
    "MG Road", "Station Road", "1st Main", "Park Street", "Church Lane",
    "Market Lane", "Rose Ave", "Victoria St.", "Baker Street", "Gandhi Road",
    "Nehru Marg", "Tilak Road", "Jawahar Nagar", "Rajpur Road", "Civil Lines",
    "LBS Marg", "Link Road", "Anna Salai", "BTM Layout", "Jayanagar",
    "Charminar Road", "Salt Lake Sector V", "Dak Bunglow", "Ring Road"
]

first_names = [
    "Ravi", "Asha", "Sunil", "Neha", "Rohit", "Priya", "Ankit", "Sneha",
    "Amit", "Kavita", "Raj", "Pooja", "Vikram", "Divya", "Sanjay", "Meera",
    "Arun", "Anjali", "Mohan", "Sarika", "Vijay", "Swati", "Nitin", "Kiran"
]

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
    
    # More realistic address generation
    place, state = random.choice(places)
    address = f"{random.randint(10, 999)} {random.choice(streets)}, {place}, {state} - {random.randint(400001, 799999)}"
    
    subtotal = sum(a for (_, _, _, a) in items)
    gst = int(round(subtotal * 0.05))
    total = subtotal + gst
    
    discount = 0
    if random.random() < 0.3:  # 30% chance
        discount = int(round(subtotal * random.uniform(0.05, 0.15)))
        total = subtotal + gst - discount
    
    # Add payment method
    payment_methods = ["CASH", "CARD", "UPI", "WALLET"]
    payment_method = random.choice(payment_methods)
    
    # Add loyalty points if applicable
    loyalty_points = 0
    if random.random() < 0.4:  # 40% chance
        loyalty_points = random.randint(5, 20)
    
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
        "total": total,
        "payment_method": payment_method,
        "loyalty_points": loyalty_points
    }

def create_receipt_base(data, width=400):
    """Create the base receipt content without effects"""
    line_height = 20
    padding = 20
    height = padding * 2 + 450 + len(data["items"]) * (line_height + 6)
    
    # Create base image with off-white background
    base_img = Image.new("RGB", (width, height), (248, 245, 240))
    draw = ImageDraw.Draw(base_img)
    
    # Try to load a receipt-like monospace font
    try:
        font_paths = [
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "C:/Windows/Fonts/consola.ttf"
        ]
        font = None
        bold_font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 14)
                bold_font = ImageFont.truetype(path, 16)
                break
        if font is None:
            font = ImageFont.load_default()
            bold_font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
        bold_font = ImageFont.load_default()
    
    # Draw receipt content
    y = padding
    
    # HEADER - centered and bold
    def draw_centered(text, font_obj=None):
        nonlocal y
        f = font_obj if font_obj else font
        text_width = draw.textlength(text, font=f)
        x = (width - text_width) / 2
        draw.text((x, y), text, font=f, fill=(0, 0, 0))
        y += line_height
    
    def draw_left(text):
        nonlocal y
        draw.text((padding, y), text, font=font, fill=(0, 0, 0))
        y += line_height
    
    def draw_right(text):
        nonlocal y
        text_width = draw.textlength(text, font=font)
        x = width - padding - text_width
        draw.text((x, y), text, font=font, fill=(0, 0, 0))
        y += line_height
    
    def draw_separator():
        nonlocal y
        draw.line([(padding, y), (width - padding, y)], fill=(0, 0, 0), width=1)
        y += line_height
    
    # Company name
    draw_centered(data["company"].upper(), bold_font)
    y += 5
    
    # Address and contact info
    draw_centered(data["address"])
    draw_centered(f"Phone: {data['phone']}")
    draw_centered(f"GSTIN: {data['gstin']}")
    y += 5
    
    draw_separator()
    
    # Bill info
    draw_left(f"Bill No: {data['bill_no']}")
    draw_left(f"Date: {data['date']}   Time: {data['time']}")
    draw_left(f"Cashier: {data['cashier']}")
    
    draw_separator()
    
    # Items header
    draw_left("Qty  Item                Rate  Amount")
    draw_separator()
    
    # Items
    for qty, name, rate, amount in data["items"]:
        if len(name) > 18: 
            name = name[:15] + "..."
        item_line = f"{qty:<4} {name:<19} {rate:>4}  {amount:>5}"
        draw_left(item_line)
    
    draw_separator()
    
    # Totals
    draw_right(f"Subtotal: {data['subtotal']:>8}")
    draw_right(f"GST (5%): {data['gst']:>8}")
    
    if data['discount'] > 0:
        draw_right(f"Discount: -{data['discount']:>7}")
    
    draw_separator()
    draw_right(f"TOTAL: {data['total']:>10}")
    draw_separator()
    
    # Payment method
    draw_left(f"Payment Method: {data['payment_method']}")
    
    # Loyalty points if applicable
    if data['loyalty_points'] > 0:
        draw_left(f"Loyalty Points Earned: {data['loyalty_points']}")
    
    y += 10
    draw_centered("Thank you for shopping with us!")
    draw_centered("Please visit again!")
    
    return base_img

def render_receipt_to_image(data, out_path="receipt.jpg"):
    """Create a realistic receipt image"""
    # Create the base receipt
    receipt_base = create_receipt_base(data)
    
    # Add some simple effects (no complex transformations that might fail)
    # Add paper texture
    texture = Image.new("RGB", receipt_base.size, (255, 255, 255))
    pixels = texture.load()
    for i in range(texture.size[0]):
        for j in range(texture.size[1]):
            if random.random() < 0.1:  # Add some texture noise
                val = random.randint(240, 255)
                pixels[i, j] = (val, val, val)
    
    receipt_img = Image.blend(receipt_base, texture, 0.05)
    
    # Add slight color temperature change
    r, g, b = receipt_img.split()
    r = ImageEnhance.Brightness(r).enhance(1.03)
    g = ImageEnhance.Brightness(g).enhance(1.01)
    receipt_img = Image.merge("RGB", (r, g, b))
    
    # Add slight noise
    pixels = receipt_img.load()
    for i in range(receipt_img.size[0]):
        for j in range(receipt_img.size[1]):
            if random.random() < 0.01:  # 1% chance of noise
                noise = random.randint(-15, 15)
                r, g, b = pixels[i, j]
                r = max(0, min(255, r + noise))
                g = max(0, min(255, g + noise))
                b = max(0, min(255, b + noise))
                pixels[i, j] = (r, g, b)
    
    # Save as high quality JPEG
    receipt_img.save(out_path, "JPEG", quality=95)
    return out_path