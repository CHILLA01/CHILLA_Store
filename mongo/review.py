
connector = MongoConnector("mongodb://localhost:27017/", "store_reviews")
coll = "reviews"

sample_reviews = [
    {"product": "MacBook Pro", "category": "Laptops", "reviewer": "Giorgi", "rating": 5, "comment": "Amazing performance", "created_at": datetime.now()},
    {"product": "MacBook Pro", "category": "Laptops", "reviewer": "Anna", "rating": 4, "comment": "A bit expensive", "created_at": datetime.now()},
    {"product": "iPhone 15", "category": "Phones", "reviewer": "Luka", "rating": 5, "comment": "Great camera", "created_at": datetime.now()},
    {"product": "iPhone 15", "category": "Phones", "reviewer": "Mari", "rating": 3, "comment": "Battery is okay", "created_at": datetime.now()},
    {"product": "Sony WH-1000XM5", "category": "Audio", "reviewer": "Nino", "rating": 5, "comment": "Best noise cancelling", "created_at": datetime.now()},
    {"product": "Sony WH-1000XM5", "category": "Audio", "reviewer": "Dato", "rating": 4, "comment": "Bulky case", "created_at": datetime.now()},
    {"product": "MacBook Pro", "category": "Laptops", "reviewer": "Sandro", "rating": 5, "comment": "Screen is beautiful", "created_at": datetime.now()},
    {"product": "iPhone 15", "category": "Phones", "reviewer": "Eka", "rating": 4, "comment": "Fast charging", "created_at": datetime.now()},
    {"product": "Sony WH-1000XM5", "category": "Audio", "reviewer": "Gio", "rating": 2, "comment": "Too expensive for me", "created_at": datetime.now()},
    {"product": "MacBook Pro", "category": "Laptops", "reviewer": "Maka", "rating": 4, "comment": "Solid build", "created_at": datetime.now()},
]

connector.db[coll].delete_many({}) # Clear old data for a fresh start
connector.insert_many(coll, sample_reviews)

avg_pipeline = [
    {"$group": {"_id": "$product", "average_rating": {"$avg": "$rating"}}}
]
print("Average Ratings:", connector.aggregate(coll, avg_pipeline))

top_product_pipeline = [
    {"$group": {"_id": "$product", "avg_rating": {"$avg": "$rating"}}},
    {"$sort": {"avg_rating": -1}},
    {"$limit": 1}
]
print("Top Rated Product:", connector.aggregate(coll, top_product_pipeline))

high_ratings_count = connector.count(coll, {"rating": {"$gte": 4}})
print(f"Reviews with rating >= 4: {high_ratings_count}")

giorgi_review = connector.find_one(coll, {"reviewer": "Giorgi"})
print("Review by Giorgi:", giorgi_review)