# seed_products.py

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fraud_detection']
products_collection = db['products']

# Optional: Clear existing products before inserting
products_collection.delete_many({})

# Sample product data
sample_products = [
    {"name": "Soap", "price": 12.00, "category": "Health & Beauty", "image": "product1.png", "description": "Gentle cleansing soap with a refreshing fragrance. Perfect for daily hygiene and skin nourishment."},
    {"name": "Shampoo", "price": 22.00, "category": "Health & Beauty", "image": "shampoo.png", "description": "Nourishing shampoo for healthy and strong hair. Enriched with natural ingredients for deep hydration."},
    {"name": "Medicine", "price": 25.00, "category": "Health & Beauty", "image": "medicine.png", "description": "Essential health supplement to support overall well-being. Carefully formulated for effectiveness."},
    {"name": "Sheet Masks", "price": 52.00, "category": "Health & Beauty", "image": "facesheets.png", "description": "Hydrating facial sheet masks infused with skin-loving nutrients for a radiant glow."},

    {"name": "Water Spray", "price": 100.00, "category": "Home & Garden", "image": "spray.png", "description": "Multipurpose water spray bottle for plants, cleaning, and household needs."},
    {"name": "Air freshener", "price": 90.00, "category": "Home & Garden", "image": "airfresh.png", "description": "Long-lasting air freshener with soothing scents to enhance your living space."},
    {"name": "Garden ToolKit", "price": 110.00, "category": "Home & Garden", "image": "gardentoll.png", "description": "Complete gardening toolkit with essential tools for planting, trimming, and maintaining your garden."},
    {"name": "Bed Sheets", "price": 115.00, "category": "Home & Garden", "image": "bed.png", "description": "Soft and stylish queen-size bed cover, crafted for comfort and elegance. Perfect fit, durable fabric, and easy maintenance for a cozy bedroom upgrade."},
    {"name": "Chair", "price": 115.00, "category": "Home & Garden", "image": "chair.png", "description": "Ergonomic and stylish chair for enhanced comfort and support in your workspace or home."},

    {"name": "Mens Shirt", "price": 35.00, "category": "Clothing", "image": "shirt.png", "description": "Classic and comfortable men's shirt, perfect for casual or formal occasions."},
    {"name": "Bell Bottom Jean", "price": 45.00, "category": "Clothing", "image": "pants.png", "description": "Retro-styled bell-bottom jeans with a comfortable fit and trendy look."},
    {"name": "BabyGCloth", "price": 25.00, "category": "Clothing", "image": "girlcloth.png", "description": "Cute and cozy clothing for baby girls, crafted from soft and breathable fabric."},
    {"name": "BabyBCloth", "price": 40.00, "category": "Clothing", "image": "boycloth.png", "description": "Stylish and comfortable clothing for baby boys, designed for durability and ease."},
    {"name": "Full piece Kurti", "price": 65.00, "category": "Clothing", "image": "kurti.png", "description": "Elegant full-piece kurti with intricate designs and a perfect blend of tradition and modern style."},

    {"name": "Marble Game", "price": 25.00, "category": "Toys & Games", "image": "game1.png", "description": "Exciting marble game set for fun-filled challenges and skillful play."},
    {"name": "Connect4", "price": 35.00, "category": "Toys & Games", "image": "game2.png", "description": "Classic strategy board game for engaging and competitive play."},
    {"name": "Hot Wheels", "price": 10.00, "category": "Toys & Games", "image": "game3.png", "description": "Fast-paced toy car set for thrilling races and imaginative play."},
    {"name": "Xl Teddy", "price": 105.00, "category": "Toys & Games", "image": "game4.png", "description": "Extra-large, super-soft teddy bear for cuddles and companionship."},
    {"name": "Chess", "price": 15.00, "category": "Toys & Games", "image": "game5.png", "description": "Classic chess set for strategic thinking and friendly matches."},

    {"name": "Keyboard", "price": 180.00, "category": "Electronics", "image": "keyborad.png", "description": "High-quality keyboard for smooth typing and gaming performance."},
    {"name": "Headphone", "price": 380.00, "category": "Electronics", "image": "headphone.png", "description": "Premium headphones with crystal-clear sound and immersive audio experience."},
    {"name": "Camera", "price": 1280.00, "category": "Electronics", "image": "camera.png", "description": "Advanced digital camera with high-resolution image capture for photography enthusiasts."},
    {"name": "One-plus", "price": 680.00, "category": "Electronics", "image": "phone.png", "description": "Sleek and powerful smartphone with cutting-edge features and seamless performance."}
]

# Insert the sample data
products_collection.insert_many(sample_products)

print("Sample products inserted successfully.")
