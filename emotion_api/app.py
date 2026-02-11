from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import cv2
import numpy as np
import os
import shutil
from model_loader import build_emotion_model

# ---------------- APP INIT ----------------
app = FastAPI(title="Emotion Detection App")

# Enable CORS for Flutter Web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your GitHub Pages URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "Emotion_little_vgg.h5")
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- LOAD MODEL ----------------
model = build_emotion_model()
model.load_weights(MODEL_PATH)

# ---------------- LOAD FACE CASCADE (SAFE) ----------------
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

if face_cascade.empty():
    raise RuntimeError(
        f"Haarcascade file not found or invalid at: {CASCADE_PATH}"
    )

class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

# =================================================
# HOME PAGE
# =================================================
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>Emotion Detection</title>
        <style>
            body {
                font-family: Arial;
                background: #f2f2f2;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .box {
                background: white;
                padding: 30px;
                border-radius: 10px;
                width: 350px;
                text-align: center;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            }
            input {
                margin: 15px 0;
            }
            button {
                padding: 10px 20px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Emotion Detection</h2>
            <form action="/predict-emotion-web" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required>
                <br>
                <button type="submit">Predict Emotion</button>
            </form>
        </div>
    </body>
    </html>
    """

# =================================================
# SAFE GET ROUTE
# =================================================
@app.get("/predict-emotion-web", response_class=HTMLResponse)
async def predict_emotion_web_get():
    return "<h2 style='text-align:center;'>Upload an image from <a href='/'>home</a></h2>"

# =================================================
# WEB PREDICTION
# =================================================
@app.post("/predict-emotion-web", response_class=HTMLResponse)
async def predict_emotion_web(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = cv2.imread(file_path)
    if img is None:
        return "<h2>Invalid image file</h2>"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "<h2 style='text-align:center;'>No face detected</h2><a href='/'>Try again</a>"

    x, y, w, h = faces[0]
    roi = gray[y:y+h, x:x+w]
    roi = cv2.resize(roi, (48, 48))
    roi = roi.astype("float32") / 255.0
    roi = roi.reshape(1, 48, 48, 1)

    preds = model.predict(roi, verbose=0)[0]
    emotion = class_labels[np.argmax(preds)]
    confidence = round(float(np.max(preds)) * 100, 2)

    return f"""
    <h1 style='text-align:center;'>Emotion: {emotion}</h1>
    <h3 style='text-align:center;'>Confidence: {confidence}%</h3>
    <div style='text-align:center;'><a href='/'>Try Another Image</a></div>
    """

# =================================================
# API FOR FLUTTER
# =================================================
@app.post("/predict-emotion/")
async def predict_emotion_api(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return {"error": "No face detected"}

    x, y, w, h = faces[0]
    roi = gray[y:y+h, x:x+w]
    roi = cv2.resize(roi, (48,48))
    roi = roi.astype("float32") / 255.0
    roi = roi.reshape(1,48,48,1)

    preds = model.predict(roi, verbose=0)[0]

    return {
        "emotion": class_labels[np.argmax(preds)],
        "confidence": round(float(np.max(preds)), 3)
    }
