import functools
import numpy as np
from datetime import datetime
# from werkzeug import secure_filename
import requests
import os


# Use a pipeline as a high-level helper

headers = {"Authorization": "Bearer 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"}
general_eye_API_URL = "https://api-inference.huggingface.co/models/SM200203102097/eyeDiseasesDetectionModel"

skinCancerAPIURL = "https://api-inference.huggingface.co/models/gianlab/swin-tiny-patch4-window7-224-finetuned-skin-cancer"

lungDiseaseAPIURL = "https://api-inference.huggingface.co/models/gianlab/swin-tiny-patch4-window7-224-finetuned-lungs-disease"


def generalEyeDetection(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(general_eye_API_URL, headers=headers, data=data)
    response = response.json()
    
    for i in range(len(response)):
        response[i]["score"] = round(response[i]["score"], 2)
    ans = ""
    for i in range(len(response)):
        ans += f"{response[i]['label']}: {response[i]['score']}~"
    return ans

def skinCancerDetection(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(skinCancerAPIURL, headers=headers, data=data)
    response = response.json()
    print(response)
    for i in range(len(response)):
        response[i]["score"] = round(response[i]["score"], 2)
    ans = ""
    for i in range(len(response)):
        ans += f"{response[i]['label']}: {response[i]['score']}~"
    return ans

def lungDiseaseDetection(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(lungDiseaseAPIURL, headers=headers, data=data)
    response = response.json()
    
    for i in range(len(response)):
        response[i]["score"] = round(response[i]["score"], 2)
    ans = ""
    for i in range(len(response)):
        ans += f"{response[i]['label']}: {response[i]['score']}~"
    return ans

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('dash', __name__, url_prefix='/dash')

# def predictCataract(img_path):
#     img = image.load_img(img_path, target_size=(224, 224))
#     img = image.img_to_array(img)
#     img = preprocess_input(img, data_format=None)
#     img = img/255.0
#     img = np.expand_dims(img, axis=0)
#     prediction = model.predict(img)
#     predicted_class_idx=np.argmax(prediction,axis=1)
#     if predicted_class_idx == 0:
#         result = "cataract"
#     else:
#         result = "normal"
#     return result


@bp.route("/dashNewScan", methods=["POST", "GET"])
def dashNewScan(doctor=None):
    doctor_id = session.get("user_id")
    db = get_db()
    if request.method == "POST":

        model = request.form["modelName"]
        firstName = request.form["firstName"]
        secondName = request.form["secondName"]
        age = request.form["age"]
        gender = request.form["gender"]
        symptoms = request.form["symptoms"]
        input_img = request.files["image"]
        status = request.form["status"]
        input_img.save(os.path.join("static/images/patients/", f"{doctor_id}{firstName}.jpg"))
        img_path = os.path.join("static/images/patients/", f"{doctor_id}{firstName}.jpg")

        if "Eye" in model:
            output_res = generalEyeDetection(img_path)
        elif "skin" in model:
            output_res = skinCancerDetection(img_path)
        else:
            output_res = lungDiseaseDetection(img_path)

        try:
            db.execute(
                "INSERT INTO scan (firstName, secondName, model, age, gender, doctor_id, symptoms, input_img, output_res, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (firstName, secondName, model, age, gender, doctor_id, symptoms, img_path, output_res, status))
            db.commit()
            print("Succesfully entered the data")
        except:
            error = "Some error"
    
    doctor = db.execute(f"SELECT * FROM user WHERE id={doctor_id}").fetchone()
    return render_template("dashnewScan.html", doctor=doctor)

@bp.route("/dashHomePage")
def dashHomePage(doctor=None):
    doctor_id = session.get("user_id")
    db = get_db()
    doctor = db.execute(f"SELECT * FROM user WHERE id={doctor_id}").fetchone()
    patients = db.execute(f"SELECT * FROM scan WHERE doctor_id={doctor_id}").fetchall()
    shared_patients = db.execute(f"SELECT * FROM share WHERE end_doctor_id={doctor_id}").fetchall()

    return render_template("dashHomePage.html", doctor=doctor, patients=patients, shared_patients=shared_patients)

@bp.route("/dashPatients")
def dashPatients():
    doctor_id = session.get("user_id")
    db = get_db()
    patients = db.execute(f"SELECT * FROM scan WHERE doctor_id={doctor_id} order by created desc" ).fetchall()
    doctor = db.execute(f"SELECT * FROM user WHERE id={doctor_id}").fetchone()
    return render_template("dashPatients.html", patients=patients, doctor=doctor)

@bp.route("/dashSharedPatients")
def dashSharedPatients():
    doctor_id = session.get("user_id")
    db = get_db()
    patients = db.execute(f"SELECT * FROM share WHERE end_doctor_id={doctor_id} order by created").fetchall()
    doctor = db.execute(f"SELECT * FROM user WHERE id={doctor_id}").fetchone()

    return render_template("dashSharedPatients.html", patients=patients, db=db, doctor=doctor)

@bp.route("/patientDetails/")
@bp.route("/patientDetails/<id>", methods=["POST", "GET"])
def patientDetails(id=None):
    doctor_id = session.get('user_id')
    db = get_db()
    doctor_name = db.execute(f"SELECT * FROM user WHERE id={doctor_id}").fetchone()
    patient = db.execute(f'SELECT * FROM scan WHERE id={id}').fetchone()
    if request.method == "POST":
        end_doctor_id = request.form["end_doctor"]
        db.execute(
            "INSERT INTO share (scan_id, og_doctor_id, end_doctor_id, og_doctor_name, firstName, secondName, created, output_res, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (id, doctor_id, end_doctor_id, doctor_name["name"], patient["firstName"], patient["secondName"], patient["created"], patient["output_res"], patient["status"])
        )
        db.commit()
        
    
    doctors = db.execute(f"SELECT * FROM user where id!={doctor_id}").fetchall()
    return render_template("dashPatientDetails.html", patient=patient, input_img=patient["input_img"], doctors=doctors, doctor=doctor_name)