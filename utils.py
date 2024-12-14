import pymongo
import bcrypt
from datetime import datetime
import os

# MongoDB Connection
def connect_to_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["food_donation_app"]

# User Authentication
def authenticate_user(db, username, password):
    user = db["users"].find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return user
    return None

# Create User
def create_user(db, username, password, role, bio, profile_picture):
    if db["users"].find_one({"username": username}):
        return False
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    profile_picture_url = upload_image_to_storage(profile_picture) if profile_picture else None
    db["users"].insert_one({
        "username": username,
        "password": hashed_pw,
        "role": role,
        "bio": bio,
        "profile_picture": profile_picture_url
    })
    return True

# Post Donation
def post_donation(db, username, food_name, expiry_date, location, contact_details, map_location, details, image_url):
    db["donations"].insert_one({
        "posted_by": username,
        "name": food_name,
        "expiry_date": expiry_date,
        "location": location,
        "contact_details": contact_details,
        "map_location": map_location,
        "details": details,
        "image_url": image_url,
        "timestamp": datetime.now()
    })

# Fetch Donations
def fetch_donations(db):
    now = datetime.now()
    db["donations"].delete_many({"expiry_date": {"$lt": now}})
    return list(db["donations"].find({}, {"_id": 1, "name": 1, "expiry_date": 1, "location": 1, "contact_details": 1, "map_location": 1, "details": 1, "posted_by": 1}))

# Upload Image
def upload_image_to_storage(image):
    upload_dir = "uploads/"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_extension = image.name.split('.')[-1]
    file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
    file_path = os.path.join(upload_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(image.getbuffer())
    return file_path

# Delete Donation
def delete_donation(db, donation_id):
    db["donations"].delete_one({"_id": donation_id})

# Create Post
def create_post(db, username, content, store_name, expiry_date, price, contact_details, map_link, upi_id, image_url):
    # Konvertera expiry_date till sträng
    expiry_date_str = expiry_date.strftime("%Y-%m-%d") if expiry_date else None
    
    post = {
        "username": username,
        "store_name": store_name,
        "content": content,
        "expiry_date": expiry_date_str,  # Använd strängversionen
        "price": float(price),
        "contact_details": contact_details,
        "map_link": map_link,
        "upi_id": upi_id,
        "image_url": image_url,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        db["posts"].insert_one(post)
        return True
    except Exception as e:
        print(f"Error creating post: {e}")
        return False

# Fetch Posts
def fetch_posts(db):
    try:
        posts = list(db["posts"].find({}).sort("timestamp", -1))
        # Säkerställ att alla nödvändiga fält finns
        for post in posts:
            post.setdefault("store_name", "Unknown Store")
            post.setdefault("content", "")
            post.setdefault("price", 0.0)
            post.setdefault("contact_details", "")
            post.setdefault("map_link", "")
            post.setdefault("upi_id", "")
            post.setdefault("image_url", None)
            post.setdefault("expiry_date", "Not specified")
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

# Create Request
def create_request(db, username, content, image_url):
    db["requests"].insert_one({
        "username": username,
        "content": content,
        "image_url": image_url,
        "timestamp": datetime.now()
    })

# Fetch Requests
def fetch_requests(db):
    return list(db["requests"].find({}, {"_id": 1, "username": 1, "content": 1, "image_url": 1, "timestamp": 1}))

# Message Functions
def send_message(db, sender, receiver, message):
    db["messages"].insert_one({
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": datetime.now()
    })

def fetch_messages(db, user1, user2):
    messages = db["messages"].find({
        "$or": [
            {"sender": user1, "receiver": user2},
            {"sender": user2, "receiver": user1}
        ]
    }).sort("timestamp", 1)
    return list(messages)