#!/usr/bin/env python3
# Ultra-Realistic Camera-Style Receipt Generator

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

def add_camera_effects(receipt_img):
    """Add camera-like effects to make it look like a photo"""
    # Convert to RGB if needed
    if receipt_img.mode != 'RGB':
        receipt_img = receipt_img.convert('RGB')
    
    # 1. Add paper texture
    texture = Image.new("RGB", receipt_img.size, (255, 255, 255))
    pixels = texture.load()
    for i in range(texture.size[0]):
        for j in range(texture.size[1]):
            if random.random() < 0.1:  # Add some texture noise
                val = random.randint(240, 255)
                pixels[i, j] = (val, val, val)
    
    receipt_img = Image.blend(receipt_img, texture, 0.05)
    
    # 2. Add perspective distortion (tilt the receipt)
    width, height = receipt_img.size
    tilt_factor = random.uniform(-0.03, 0.03)
    
    # Create a new image for the transformed receipt
    transformed = Image.new("RGB", (int(width * 1.1), int(height * 1.1)), (240, 240, 235))
    
    # Apply perspective transformation
    for y in range(height):
        # Calculate the shift for this row (more shift at the bottom)
        shift = int(tilt_factor * (height - y))
        
        # Extract the row from the original image
        row = receipt_img.crop((0, y, width, y+1))
        
        # Paste the row with the calculated shift
        transformed.paste(row, (shift, y))
    
    receipt_img = transformed
    
    # 3. Add shadow effect
    shadow_size = (receipt_img.width + 20, receipt_img.height + 20)
    final_img = Image.new("RGB", shadow_size, (240, 240, 235))
    
    # Create shadow
    shadow = Image.new("RGB", (receipt_img.width, receipt_img.height), (0, 0, 0))
    shadow_mask = Image.new("L", (receipt_img.width, receipt_img.height), 0)
    shadow_draw = ImageDraw.Draw(shadow_mask)
    
    # Draw a gradient shadow
    for i in range(10):
        alpha = 30 - i * 3
        shadow_draw.rectangle([(i, i), (receipt_img.width-i, receipt_img.height-i)], 
                            outline=alpha)
    
    shadow.putalpha(shadow_mask)
    final_img.paste(shadow, (10, 10), shadow)
    
    # Paste the receipt on top of the shadow
    final_img.paste(receipt_img, (5, 5))
    
    # 4. Add lighting effects (vignette and glare)
    vignette = Image.new("L", final_img.size, 255)
    vignette_draw = ImageDraw.Draw(vignette)
    
    # Draw vignette (darker corners)
    width, height = final_img.size
    for x in range(width):
        for y in range(height):
            # Calculate distance from center (0-1)
            dx = abs(x - width/2) / (width/2)
            dy = abs(y - height/2) / (height/2)
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Apply vignette effect
            vignette_value = int(255 * (1 - distance * 0.3))
            vignette.putpixel((x, y), vignette_value)
    
    # Apply vignette
    final_img = Image.composite(final_img, Image.new("RGB", final_img.size, (0, 0, 0)), vignette)
    
    # Add random glare spot
    glare = Image.new("L", final_img.size, 0)
    glare_draw = ImageDraw.Draw(glare)
    
    glare_x = random.randint(width//4, width*3//4)
    glare_y = random.randint(height//4, height*3//4)
    glare_radius = random.randint(30, 70)
    
    for x in range(glare_x - glare_radius, glare_x + glare_radius):
        for y in range(glare_y - glare_radius, glare_y + glare_radius):
            dist = math.sqrt((x - glare_x)**2 + (y - glare_y)**2)
            if dist < glare_radius:
                intensity = int(200 * (1 - dist/glare_radius))
                if 0 <= x < width and 0 <= y < height:
                    current = glare.getpixel((x, y))
                    glare.putpixel((x, y), max(current, intensity))
    
    # Apply glare with screen blend mode
    glare_rgb = Image.merge("RGB", (glare, glare, glare))
    final_img = Image.blend(final_img, glare_rgb, 0.1)
    
    # 5. Add slight blur and color adjustment
    final_img = final_img.filter(ImageFilter.GaussianBlur(radius=0.7))
    
    # Adjust color temperature (slightly warmer)
    r, g, b = final_img.split()
    r = ImageEnhance.Brightness(r).enhance(1.03)
    g = ImageEnhance.Brightness(g).enhance(1.01)
    final_img = Image.merge("RGB", (r, g, b))
    
    # 6. Add slight noise
    pixels = final_img.load()
    for i in range(final_img.size[0]):
        for j in range(final_img.size[1]):
            if random.random() < 0.01:  # 1% chance of noise
                noise = random.randint(-15, 15)
                r, g, b = pixels[i, j]
                r = max(0, min(255, r + noise))
                g = max(0, min(255, g + noise))
                b = max(0, min(255, b + noise))
                pixels[i, j] = (r, g, b)
    
    return final_img

def generate_ultra_realistic_receipt(out_path="receipt.jpg"):
    """Generate a complete realistic receipt that looks like a photo"""
    # Generate receipt data
    data = generate_receipt_data()
    
    # Create the base receipt
    receipt_base = create_receipt_base(data)
    
    # Add camera effects
    final_receipt = add_camera_effects(receipt_base)
    
    # Save as high quality JPEG
    final_receipt.save(out_path, "JPEG", quality=95)
    return out_path, data

if __name__ == "__main__":
    # Generate multiple receipts
    num_receipts = 3
    for i in range(num_receipts):
        filename, data = generate_ultra_realistic_receipt(f"camera_receipt_{i+1}.jpg")
        print(f"Generated {filename} (Bill No: {data['bill_no']})")