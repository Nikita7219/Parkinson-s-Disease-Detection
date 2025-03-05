import json
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing import image
from PIL import Image 
from flask import Flask, render_template, request, url_for, redirect,session
import mysql.connector


with open("config.json", "r") as c:
    params = json.load(c)["params"]
import numpy as np

app = Flask(__name__, template_folder="template", static_url_path='/static', static_folder='uploaded_files')

app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost", port=port_number, user="user_name", password="*****", database="database_name")
cursor=conn.cursor()

Model = load_model(r"static\models\parkinsons_detection_ensemble.h5")


def model_predict(img_path, model):
    
    result = {}
    img = image.load_img(img_path, target_size=(64, 64))

    # Preprocessing the image
    x = image.img_to_array(img)
    
    ## Scaling
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    if preds == 0:
        result["prediction"] = "The patient is Healthy"
        result["description"] = "I'm glad to hear that you're feeling well. Your recent tests show that you do not have Parkinson's disease. I know that you may have been concerned about your health, and I am glad that we can put your worries to rest. However, it is important to continue to monitor your health and see your doctor for regular checkups. Take care of yourself.....!!"

    else:
        result["prediction"] = "The patient has Parkinson's Disease"
        result["description"] = "I'm so sorry to tell you that you have Parkinson's disease. This is a condition that affects the way your brain controls your movements. It can cause tremors, stiffness, and difficulty with balance and coordination. However, there are treatments that can help slow the progression of the disease and improve your quality of life. Take care of yourself.....!!"

    return result

def is_valid_image(file_path):
    try:
        # Read the uploaded image using OpenCV
        image = cv2.imread(file_path)
        elab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        # split the channels
        el, ea, eb = cv2.split(elab)
        # obtain difference between A and B channel at every pixel location
        de = abs(ea-eb)
        # find the mean of this difference
        mean_e = np.mean(de)
        
        # Check if the image is not None and has specific dimensions and color channels
        if image is not None:
                        
            if int(mean_e) == 0:
                return True
            else:
                return False

    except Exception as e:
        print(str(e))
    # return False


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
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `user` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    user=cursor.fetchall()
    if len(user)>0:
        session['user_id']=user[0][0]
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
        if filepath and is_valid_image(filepath):
            result["predict"] = model_predict(filepath, Model)
            result["image"] = f.filename
            result["isPredicted"] = True
            return render_template(
            "prediction.html", result=result
            )
        else:
            result["image"] = f.filename
            result["error"] = "This image is not Valid..!!"
            result["isPredicted"] = False
            return render_template(
            "prediction.html", result=result
            )
    
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    # Check if email already exists
    cursor.execute("SELECT * FROM `user` WHERE `email` = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return '''<script>alert("Email already exists! Please use a different email."); window.location.href="/";</script>'''

    # Insert new user if email doesn't exist
    cursor.execute("INSERT INTO `user` (`user_id`,`name`,`email`,`password`) VALUES (NULL, %s, %s, %s)", (name, email, password))
    conn.commit()

    return '''<script>alert("Signup successful! Please log in."); window.location.href="/";</script>'''


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
