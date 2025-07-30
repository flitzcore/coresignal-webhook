from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')  # Replace with your actual MongoDB URI
client = MongoClient(MONGO_URI)

# Access database and collection
db_mvp = client["turf_mvp"]
webhook_data_col = db_mvp["webhook_data"]

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the request body data
        data = request.get_json()
        
        # Create document with timestamp and data
        webhook_document = {
            "timestamp": datetime.utcnow(),
            "data": data
        }
        
        # Insert into MongoDB collection
        result = webhook_data_col.insert_one(webhook_document)
        
        return jsonify({
            "success": True,
            "message": "Webhook data saved successfully",
            "document_id": str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error saving webhook data: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)