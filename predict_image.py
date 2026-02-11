import cv2
import numpy as np
from model_loader import build_emotion_model

# Load model architecture
model = build_emotion_model()

# Load weights ONLY
model.load_weights("Emotion_little_vgg.h5")

class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

face_classifier = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)

def predict_emotion(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "No face detected"

    for (x,y,w,h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (48,48))
        roi = roi.astype("float32") / 255.0
        roi = roi.reshape(1,48,48,1)

        preds = model.predict(roi, verbose=0)[0]
        return class_labels[np.argmax(preds)]

print("Predicted Emotion:", predict_emotion("test_images/sad.jpg"))
