from flask import Flask
import pyrebase
import firebase_admin
from firebase_admin import auth as firebase_admin_auth, credentials, firestore

from routes import configure_routes

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Firebase configuration
firebaseConfig = {
  "apiKey": "AIzaSyDMbl0549XQXckH-bkqkZrZgnN-3C4DJEs",
  "authDomain": "eduall-d42d8.firebaseapp.com",
  "projectId": "eduall-d42d8",
  "storageBucket": "eduall-d42d8.appspot.com",
  "messagingSenderId": "173044320418",
  "appId": "1:173044320418:web:8205dddd73788c415c2ffb",
  "databaseURL": "" ,
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Initializing Firebase Admin SDK
cred = credentials.Certificate("eduall.json") 
firebase_admin.initialize_app(cred)

# Initializing Firestore
db = firestore.client()

# Call a function to configure routes
configure_routes(app, auth, firebase_admin_auth, db)

if __name__ == "__main__":
    app.run(debug=True)
