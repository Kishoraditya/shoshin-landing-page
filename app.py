from flask import Flask, render_template, request
from pymongo import MongoClient
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_secret_key')

# MongoDB Atlas connection
mongodb_uri = os.environ.get('MONGODB_URI')
if mongodb_uri:
    # URL encode the username and password
    username = quote_plus(os.environ.get('MONGO_USERNAME', ''))
    password = quote_plus(os.environ.get('MONGO_PASSWORD', ''))
    
    # Construct the full connection string
    connection_string = mongodb_uri.replace('<username>', username).replace('<password>', password)
    
    client = MongoClient(connection_string)
    db = client.get_database('shoshin_db')  # or your actual database name
    subscribers = db.subscribers
else:
    print("Warning: MONGODB_URI not set. Running without database connection.")
    subscribers = None
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            subscribers.insert_one({'email': email})
            return render_template('index.html', message='Thank you for subscribing!')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
