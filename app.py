import json
import os
import cv2
import numpy as np
import gdown  
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector

# Load config
with open("config.json", "r") as c:
    params = json.load(c)["params"]

app = Flask(__name__, template_folder="template", static_url_path='/static', static_folder='uploaded_files')
app.secret_key = os.urandom(24)

# Database connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="nikita",
    password="Nikita@7219",
    database="nikita"
)
cursor = conn.cursor()

# Google Drive Model File ID
GOOGLE_DRIVE_FILE_ID = "1n7ULGu9XgitFHDjcOuil0OV4dbojgk5c"  # Replace with your actual file ID

# Path to save the downloaded model
MODEL_PATH = "static/models/parkinsons_detection_ensemble.h5"

# Function to download the model from Google Drive
def download_model():
    if not os.path.exists(MODEL_PATH):  # Download only if not already downloaded
        url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print("Model downloaded successfully.")

# Download the model before loading
download_model()

# Load the model
Model = load_model(MODEL_PATH)
print("Model loaded successfully.")

# Function to predict Parkinson's Disease
def model_predict(img_path, model):
    result = {}
    img = image.load_img(img_path, target_size=(64, 64))

    # Preprocessing
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # Prediction
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    
    if preds == 0:
        result["prediction"] = "The patient is Healthy"
        result["description"] = "I'm glad to hear that you're feeling well. Your tests show that you do not have Parkinson's disease."
    else:
        result["prediction"] = "The patient has Parkinson's Disease"
        result["description"] = "I'm sorry to inform you that you have Parkinson's disease. Consult a doctor for further diagnosis."

    return result

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/index")
def index():
    if 'user_id' in session:
        return render_template("index.html", params=params)
    else:
        return redirect('/')

@app.route("/login_validation", methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM `user` WHERE `email` = %s AND `password` = %s", (email, password))
    user = cursor.fetchall()

    if user:
        session['user_id'] = user[0][0]
        return redirect('/index')
    else:
        return redirect('/')

@app.route("/uploader", methods=["GET", "POST"])
def uploader():
    if request.method == "POST":
        f = request.files["file1"]
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, "uploaded_files", secure_filename(f.filename))
        f.save(filepath)
        
        result = {}
        result["predict"] = model_predict(filepath, Model)
        result["image"] = f.filename
        result["isPredicted"] = True
        return render_template("prediction.html", result=result)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    # Check if email exists
    cursor.execute("SELECT * FROM `user` WHERE `email` = %s", (email,))
    if cursor.fetchone():
        return '''<script>alert("Email already exists! Use a different email."); window.location.href="/";</script>'''

    # Insert new user
    cursor.execute("INSERT INTO `user` (`user_id`, `name`, `email`, `password`) VALUES (NULL, %s, %s, %s)", (name, email, password))
    conn.commit()

    return '''<script>alert("Signup successful! Please log in."); window.location.href="/";</script>'''

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
