from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
import certifi

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_secret_key')

# MongoDB Atlas connection
mongodb_uri = os.environ.get('MONGODB_URI')
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')

if mongodb_uri:
     # URL encode the username and password
    username = quote_plus(mongo_username)
    password = quote_plus(mongo_password)
    
    # Construct the full connection string
    connection_string = mongodb_uri.replace('<username>', username).replace('<password>', password)
    
    client = MongoClient(connection_string, 
                     tls=True, 
                     tlsAllowInvalidCertificates=True,
                     tlsCAFile=certifi.where())
    
    db = client.get_database('shoshin_db')  # or your actual database name
    subscribers = db.subscribers

# Test the connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("Warning: MONGODB_URI not set. Running without database connection.")
    subscribers = None
    
import logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        print(f"Received email: {email}")
        if email and subscribers:
            try:
                result = subscribers.insert_one({'email': email})
                print(f"Inserted email: {email} with ID: {result.inserted_id}")
                return jsonify({"message": "Thank you for subscribing!"}), 200
            except Exception as e:
                print(f"Database error: {e}")
                return jsonify({"error": "An error occurred. Please try again later."}), 500
        else:
            print("Email not provided or subscribers collection not available")
            return jsonify({"error": "Invalid request"}), 400
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
