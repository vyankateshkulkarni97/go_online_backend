
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goonline.settings")
django.setup()

from go_online.models import Category, Product
from django.utils.text import slugify

products = [
    # Fashion (10)
    ("fashion", "Men's Casual T-Shirt", "FASH001", "Cotton T-shirt", 999, 599),
    ("fashion", "Women's Handbag", "FASH002", "Stylish handbag", 1999, 1299),
    ("fashion", "Running Shoes", "FASH003", "Comfortable running shoes", 2499, 1799),
    ("fashion", "Denim Jeans", "FASH004", "Casual denim jeans", 1599, 1199),
    ("fashion", "Men's Formal Shirt", "FASH005", "Slim fit formal shirt", 1499, 999),
    ("fashion", "Women's Kurti", "FASH006", "Printed cotton kurti", 1299, 799),
    ("fashion", "Men's Hoodie", "FASH007", "Warm casual hoodie", 1999, 1399),
    ("fashion", "Women's Dress", "FASH008", "Elegant casual dress", 2499, 1699),
    ("fashion", "Leather Belt", "FASH009", "Classic leather belt", 799, 499),
    ("fashion", "Sunglasses", "FASH010", "UV protection sunglasses", 1299, 799),

    # Mobiles (10)
    ("mobiles", "Smartphone 128GB", "MOB001", "128GB smartphone", 24999, 21999),
    ("mobiles", "Mobile Cover", "MOB002", "Protective phone cover", 499, 299),
    ("mobiles", "Fast Charger", "MOB003", "Fast charging adapter", 1499, 999),
    ("mobiles", "USB-C Cable", "MOB004", "Durable USB-C charging cable", 499, 299),
    ("mobiles", "Wireless Earbuds", "MOB005", "Bluetooth wireless earbuds", 2499, 1799),
    ("mobiles", "Power Bank 20000mAh", "MOB006", "High capacity power bank", 2499, 1899),
    ("mobiles", "Screen Protector", "MOB007", "Tempered glass screen guard", 399, 199),
    ("mobiles", "Smartphone 256GB", "MOB008", "256GB smartphone", 32999, 28999),
    ("mobiles", "Car Mobile Holder", "MOB009", "Adjustable mobile holder", 799, 499),
    ("mobiles", "Wireless Charging Pad", "MOB010", "Wireless phone charging pad", 1999, 1399),

    # Electronics (10)
    ("electronics", "Wireless Headphones", "ELEC001", "Wireless headphones", 2999, 1999),
    ("electronics", "Bluetooth Speaker", "ELEC002", "Portable speaker", 2499, 1799),
    ("electronics", "Wireless Mouse", "ELEC003", "Wireless computer mouse", 999, 699),
    ("electronics", "Mechanical Keyboard", "ELEC004", "RGB mechanical keyboard", 3499, 2499),
    ("electronics", "USB Flash Drive 64GB", "ELEC005", "64GB USB flash drive", 899, 599),
    ("electronics", "External SSD 1TB", "ELEC006", "Portable 1TB solid state drive", 8999, 6999),
    ("electronics", "Webcam", "ELEC007", "Full HD USB webcam", 2499, 1799),
    ("electronics", "Computer Monitor 24-inch", "ELEC008", "24-inch Full HD monitor", 11999, 9999),
    ("electronics", "Laptop Stand", "ELEC009", "Adjustable laptop stand", 1499, 999),
    ("electronics", "HDMI Cable", "ELEC010", "High speed HDMI cable", 699, 399),

    # Beauty (10)
    ("beauty", "Face Care Kit", "BEAUTY001", "Daily skincare kit", 1499, 999),
    ("beauty", "Face Wash", "BEAUTY002", "Daily face cleanser", 399, 299),
    ("beauty", "Moisturizer", "BEAUTY003", "Daily hydrating moisturizer", 599, 399),
    ("beauty", "Sunscreen SPF 50", "BEAUTY004", "Broad spectrum sunscreen", 799, 599),
    ("beauty", "Shampoo", "BEAUTY005", "Daily hair cleansing shampoo", 499, 349),
    ("beauty", "Hair Conditioner", "BEAUTY006", "Nourishing hair conditioner", 499, 349),
    ("beauty", "Body Lotion", "BEAUTY007", "Moisturizing body lotion", 399, 279),
    ("beauty", "Lip Balm", "BEAUTY008", "Hydrating lip balm", 199, 129),
    ("beauty", "Makeup Brush Set", "BEAUTY009", "Professional makeup brushes", 999, 699),
    ("beauty", "Perfume", "BEAUTY010", "Everyday fragrance", 1499, 999),

    # Home (10)
    ("home", "Decorative Table Lamp", "HOME001", "Modern table lamp", 1999, 1499),
    ("home", "Wall Clock", "HOME002", "Decorative wall clock", 999, 699),
    ("home", "Cushion Cover Set", "HOME003", "Decorative cushion covers", 799, 499),
    ("home", "Bedsheet Set", "HOME004", "Cotton bedsheet with pillow covers", 1999, 1399),
    ("home", "Curtains", "HOME005", "Window curtain pair", 1499, 999),
    ("home", "Storage Organizer", "HOME006", "Multipurpose storage organizer", 999, 649),
    ("home", "Flower Vase", "HOME007", "Decorative ceramic flower vase", 899, 599),
    ("home", "Wall Art", "HOME008", "Modern decorative wall art", 1299, 899),
    ("home", "Door Mat", "HOME009", "Anti-slip entrance door mat", 499, 299),
    ("home", "Laundry Basket", "HOME010", "Foldable laundry basket", 799, 549),

    # Appliances (10)
    ("appliances", "Electric Kettle", "APP001", "Electric water kettle", 1999, 1499),
    ("appliances", "Mixer Grinder", "APP002", "Kitchen mixer grinder", 3999, 2999),
    ("appliances", "Air Fryer", "APP003", "Compact electric air fryer", 6999, 5499),
    ("appliances", "Toaster", "APP004", "Two slice bread toaster", 1999, 1399),
    ("appliances", "Rice Cooker", "APP005", "Electric rice cooker", 2999, 2199),
    ("appliances", "Induction Cooktop", "APP006", "Electric induction cooktop", 3499, 2499),
    ("appliances", "Hand Blender", "APP007", "Portable hand blender", 1499, 999),
    ("appliances", "Room Heater", "APP008", "Electric room heater", 2999, 2199),
    ("appliances", "Vacuum Cleaner", "APP009", "Compact home vacuum cleaner", 5999, 4499),
    ("appliances", "Steam Iron", "APP010", "Non-stick steam iron", 1999, 1299),

    # Toys, Baby & Kids (10)
    ("toys-baby-kids", "Building Blocks", "TOY001", "Kids building blocks", 999, 699),
    ("toys-baby-kids", "Soft Teddy Bear", "TOY002", "Soft plush teddy bear", 799, 499),
    ("toys-baby-kids", "Remote Control Car", "TOY003", "Rechargeable RC car", 1999, 1399),
    ("toys-baby-kids", "Baby Feeding Bottle", "TOY004", "BPA-free baby feeding bottle", 499, 299),
    ("toys-baby-kids", "Kids School Backpack", "TOY005", "Lightweight school backpack", 1299, 899),
    ("toys-baby-kids", "Coloring Book Set", "TOY006", "Drawing and coloring book set", 399, 249),
    ("toys-baby-kids", "Toy Train Set", "TOY007", "Kids electric toy train set", 1499, 999),
    ("toys-baby-kids", "Baby Blanket", "TOY008", "Soft baby blanket", 999, 699),
    ("toys-baby-kids", "Kids Puzzle Game", "TOY009", "Educational puzzle game", 599, 399),
    ("toys-baby-kids", "Toy Doctor Set", "TOY010", "Pretend play doctor kit", 999, 649),

    # Food & Health (10)
    ("food-health", "Dry Fruits Pack", "FOOD001", "Mixed dry fruits", 999, 799),
    ("food-health", "Protein Shaker", "FOOD002", "Reusable shaker bottle", 599, 399),
    ("food-health", "Almonds 500g", "FOOD003", "Premium whole almonds", 699, 549),
    ("food-health", "Cashews 500g", "FOOD004", "Premium cashew nuts", 799, 649),
    ("food-health", "Green Tea", "FOOD005", "Green tea bags pack", 399, 299),
    ("food-health", "Honey 500g", "FOOD006", "Natural honey", 499, 349),
    ("food-health", "Oats 1kg", "FOOD007", "Whole grain rolled oats", 299, 229),
    ("food-health", "Lunch Box", "FOOD008", "Reusable insulated lunch box", 899, 599),
    ("food-health", "Digital Weighing Scale", "FOOD009", "Digital body weight scale", 1499, 999),
    ("food-health", "Water Bottle", "FOOD010", "Reusable stainless steel bottle", 799, 549),

    # Auto Accessories (10)
    ("auto-accessories", "Car Phone Holder", "AUTO001", "Dashboard phone holder", 799, 499),
    ("auto-accessories", "Car Cleaning Kit", "AUTO002", "Vehicle cleaning kit", 1299, 899),
    ("auto-accessories", "Car Vacuum Cleaner", "AUTO003", "Portable car vacuum cleaner", 2499, 1799),
    ("auto-accessories", "Car Air Freshener", "AUTO004", "Long lasting car air freshener", 399, 249),
    ("auto-accessories", "Car Seat Cushion", "AUTO005", "Comfortable seat cushion", 1499, 999),
    ("auto-accessories", "Car Sunshade", "AUTO006", "Foldable windshield sunshade", 699, 449),
    ("auto-accessories", "Tyre Pressure Gauge", "AUTO007", "Digital tyre pressure gauge", 999, 699),
    ("auto-accessories", "Car Charger", "AUTO008", "Dual USB car charger", 799, 499),
    ("auto-accessories", "Bike Phone Mount", "AUTO009", "Handlebar mobile phone mount", 899, 599),
    ("auto-accessories", "Car Microfiber Cloth", "AUTO010", "Scratch-safe cleaning cloth set", 499, 299),

    # Sports & Fitness (10)
    ("sports-fitness", "Yoga Mat", "SPORT001", "Non-slip yoga mat", 1499, 999),
    ("sports-fitness", "Skipping Rope", "SPORT002", "Fitness skipping rope", 499, 299),
    ("sports-fitness", "Dumbbell Set", "SPORT003", "Home workout dumbbell set", 2499, 1799),
    ("sports-fitness", "Resistance Bands", "SPORT004", "Resistance bands workout set", 999, 649),
    ("sports-fitness", "Cricket Bat", "SPORT005", "Practice cricket bat", 1999, 1399),
    ("sports-fitness", "Football", "SPORT006", "Durable training football", 999, 699),
    ("sports-fitness", "Badminton Racket", "SPORT007", "Lightweight badminton racket", 1499, 999),
    ("sports-fitness", "Sports Water Bottle", "SPORT008", "Leakproof sports water bottle", 599, 399),
    ("sports-fitness", "Gym Gloves", "SPORT009", "Padded workout gloves", 699, 449),
    ("sports-fitness", "Fitness Tracker", "SPORT010", "Activity and step tracker", 2999, 2199),

    # Furniture (10)
    ("furniture", "Office Chair", "FURN001", "Ergonomic office chair", 7999, 5999),
    ("furniture", "Study Table", "FURN002", "Wooden study table", 5999, 4499),
    ("furniture", "Bookshelf", "FURN003", "Multipurpose storage bookshelf", 4999, 3499),
    ("furniture", "Bedside Table", "FURN004", "Compact bedside table", 2999, 1999),
    ("furniture", "Computer Desk", "FURN005", "Modern computer workstation desk", 6999, 4999),
    ("furniture", "Dining Chair", "FURN006", "Contemporary dining chair", 2499, 1799),
    ("furniture", "Shoe Rack", "FURN007", "Multi-tier shoe storage rack", 1999, 1299),
    ("furniture", "Wardrobe Organizer", "FURN008", "Clothes storage organizer", 1499, 999),
    ("furniture", "Coffee Table", "FURN009", "Modern living room coffee table", 3999, 2799),
    ("furniture", "Folding Stool", "FURN010", "Compact folding stool", 999, 649),

    # Books (10)
    ("books", "Python Programming Book", "BOOK001", "Learn Python programming", 899, 699),
    ("books", "Web Development Guide", "BOOK002", "Web development fundamentals", 799, 599),
    ("books", "Django for Beginners", "BOOK003", "Introduction to Django development", 999, 749),
    ("books", "Learning JavaScript", "BOOK004", "JavaScript programming fundamentals", 899, 649),
    ("books", "Data Structures and Algorithms", "BOOK005", "DSA concepts and practice", 1199, 899),
    ("books", "Database Design Guide", "BOOK006", "Database modeling and SQL basics", 999, 749),
    ("books", "Machine Learning Basics", "BOOK007", "Beginner machine learning guide", 1299, 999),
    ("books", "Clean Code", "BOOK008", "A guide to writing maintainable code", 1199, 899),
    ("books", "System Design Handbook", "BOOK009", "Introduction to scalable systems", 1099, 799),
    ("books", "Linux Command Line Guide", "BOOK010", "Linux terminal and shell scripting", 899, 649),
]

created = 0
updated = 0

for category_slug, name, sku, description, mrp, price in products:
    category = Category.objects.get(slug=category_slug)

    _, was_created = Product.objects.update_or_create(
        sku=sku,
        defaults={
            "category": category,
            "name": name,
            "slug": slugify(name),
            "description": description,
            "mrp": mrp,
            "selling_price": price,
            "is_active": True,
            "is_featured": False,
        },
    )

    if was_created:
        created += 1
    else:
        updated += 1

print(f"New products added: {created}")
print(f"Existing products updated: {updated}")
print(f"Total products in database: {Product.objects.count()}")
