#!/usr/bin/env python3
# Receipt generator logic
import random
import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# Expanded lists for more variety
fruit_names = [
    "Apple", "Banana", "Grapes", "Orange", "Papaya", "Mango",
    "Pineapple", "Kiwi", "Pear", "Guava", "Strawberry", "Blueberry",
    "Watermelon", "Pomegranate", "Cherry", "Peach", "Plum", "Apricot"
]

company_prefixes = [
    "Fresh", "Green", "Daily", "Urban", "Organic", "Prime",
    "Budget", "Harvest", "Royal", "Metro", "Super", "Mega",
    "Family", "City", "Friendly", "Quick", "Value", "Best"
]

company_suffixes = [
    "Mart", "Grocery", "Store", "Bazaar", "Grocers", "Market",
    "Provision", "Center", "Corner", "Depot", "Shop", "Supermarket"
]

places = [
    "Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Nagpur", "Surat",
    "Bhopal", "Indore", "Patna", "Vadodara", "Ghaziabad", "Ludhiana"
]

streets = [
    "MG Road", "Station Road", "1st Main", "Park Street", "Church Lane",
    "Market Lane", "Rose Ave", "Victoria St.", "Baker Street", "Gandhi Road",
    "Nehru Marg", "Tilak Road", "Jawahar Nagar", "Rajpur Road", "Civil Lines"
]

def random_gstin():
    state = f"{random.randint(1,35):02d}"
    pan = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + \
          ''.join(random.choices("0123456789", k=4)) + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    entity = random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return state + pan + entity + "Z" + random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def generate_receipt_data():
    num_items = random.randint(2, 8)
    items = []
    for _ in range(num_items):
        name = random.choice(fruit_names)
        desc_options = ["(1kg)", "(Dozen)", "(500g)", "(250g)", "(per piece)", "(bunch)"]
        desc = random.choice(desc_options)
        qty = random.randint(1, 5)
        rate = random.choice([30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 140, 150]) + random.randint(0, 49)
        amount = qty * rate
        items.append((qty, f"{name} {desc}", rate, amount))
    
    company = f"{random.choice(company_prefixes)} {random.choice(company_suffixes)}"
    gstin = random_gstin()
    phone = f"+91 {random.randint(90000, 99999)} {random.randint(10000, 99999)}"
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    time = datetime.datetime.now().strftime("%I:%M %p")
    cashier = random.choice(["Ravi", "Asha", "Sunil", "Neha", "Rohit", "Priya", "Ankit", "Sneha"])
    bill_no = f"{random.randint(1000, 9999):04d}"
    place = random.choice(places)
    address = f"{random.randint(10, 999)} {random.choice(streets)}, {place} - {random.randint(400001, 799999)}"
    
    subtotal = sum(a for (_, _, _, a) in items)
    gst = int(round(subtotal * 0.05))
    total = subtotal + gst
    
    # Add discount randomly (about 30% of receipts)
    discount = 0
    if random.random() < 0.3:
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

def render_receipt_to_image(data, out_path="receipt_output.png", width=400):
    # Calculate height based on number of items
    line_height = 20
    padding = 20
    height = padding * 2 + 400 + len(data["items"]) * (line_height + 6)
    
    img = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(img)
    
    # Try to load a monospace font for better alignment
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "C:/Windows/Fonts/consola.ttf"
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
    
    x = padding
    y = padding
    
    def draw_line(s="", align="left", font_size=None):
        nonlocal y
        current_font = font
        if font_size:
            try:
                current_font = ImageFont.truetype(font.path, font_size) if hasattr(font, 'path') else font
            except:
                pass
                
        if align == "center":
            text_width = draw.textlength(s, font=current_font)
            draw.text(((width - text_width) / 2, y), s, font=current_font, fill=0)
        elif align == "right":
            text_width = draw.textlength(s, font=current_font)
            draw.text((width - padding - text_width, y), s, font=current_font, fill=0)
        else:
            draw.text((x, y), s, font=current_font, fill=0)
        y += line_height
    
    # Header
    draw_line(data["company"].upper(), "center", 16)
    draw_line()
    draw_line(data["address"], "center")
    draw_line(f"Phone: {data['phone']}", "center")
    draw_line(f"GSTIN: {data['gstin']}", "center")
    draw_line("-" * 40)
    
    # Bill info
    draw_line(f"Bill No: {data['bill_no']}")
    draw_line(f"Date: {data['date']}    Time: {data['time']}")
    draw_line(f"Cashier: {data['cashier']}")
    draw_line("-" * 40)
    
    # Items header
    draw_line("Qty  Item                Rate  Amount")
    draw_line("-" * 40)
    
    # Items
    for qty, name, rate, amount in data["items"]:
        if len(name) > 18:
            name = name[:15] + "..."
        item_line = f"{qty:<4} {name:<19} {rate:>4}  {amount:>5}"
        draw_line(item_line)
    
    draw_line("-" * 40)
    
    # Totals
    draw_line(f"Subtotal: {data['subtotal']:>28}")
    draw_line(f"GST (5%): {data['gst']:>28}")
    
    if data['discount'] > 0:
        draw_line(f"Discount: -{data['discount']:>26}")
    
    draw_line("-" * 40)
    draw_line(f"TOTAL: {data['total']:>30}")
    draw_line("-" * 40)
    
    # Footer
    draw_line("Thank you for shopping with us!", "center")
    draw_line("Please visit again!", "center")
    
    img.save(out_path)
    return out_path

if __name__ == '__main__':
    # Test: generate a receipt locally
    receipt_data = generate_receipt_data()
    filename = f"receipt_{receipt_data['bill_no']}.png"
    render_receipt_to_image(receipt_data, out_path=filename)
    print(f"Saved {filename}")
