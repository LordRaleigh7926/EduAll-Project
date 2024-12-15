from flask import Flask
import pyrebase
import firebase_admin
from firebase_admin import auth as firebase_admin_auth, credentials, firestore

from routes import configure_routes

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Firebase configuration
firebaseConfig = {
  "apiKey": "",
  "authDomain": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
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
