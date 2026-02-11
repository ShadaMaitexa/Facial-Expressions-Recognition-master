# Emotion Detection API - Deployment Guide

## 📱 Integration with Flutter Mobile App

Your API has a dedicated endpoint for Flutter: `POST /predict-emotion/`

### API Endpoint
```
POST /predict-emotion/
```

### Request Format
- **Content-Type**: `multipart/form-data`
- **Body**: Image file with key `file`

### Response Format
```json
{
  "emotion": "Happy",
  "confidence": 0.982
}
```
OR
```json
{
  "error": "No face detected"
}
```

---

## 🚀 Deployment Options

### **Option 1: Local Testing with ngrok (Fastest for Testing)**

#### Step 1: Install ngrok
Download from: https://ngrok.com/download

#### Step 2: Run your FastAPI app locally
```bash
cd c:\Users\shadajifrin\Desktop\Projects\Facial-Expressions-Recognition-master\emotion_api
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

#### Step 3: In a new terminal, run ngrok
```bash
ngrok http 8000
```

#### Step 4: Use the ngrok URL in your Flutter app
ngrok will provide a URL like: `https://abc123.ngrok.io`

**Flutter Integration:**
```dart
final url = 'https://abc123.ngrok.io/predict-emotion/';
// Use this URL in your HTTP requests
```

**⚠️ Note:** ngrok free URLs change every time you restart. Upgrade to paid for permanent URLs.

---

### **Option 2: Render.com (Free & Recommended for Production)**

#### Step 1: Create Render Account
Sign up at: https://render.com

#### Step 2: Create a new Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository (or use "Deploy from Git URL")
3. Set **Root Directory** to: `emotion_api`
4. Render will auto-detect the Dockerfile

#### Step 3: Configure
- **Name**: emotion-detection-api
- **Runtime**: Docker
- **Plan**: Free
- **Health Check Path**: `/`

#### Step 4: Deploy
Click **"Create Web Service"** - Render will build and deploy automatically!

#### Step 5: Get Your URL
Render will provide a URL like: `https://emotion-detection-api.onrender.com`

**Flutter Integration:**
```dart
final url = 'https://emotion-detection-api.onrender.com/predict-emotion/';
```

**⚠️ Note:** Free tier spins down after 15 minutes of inactivity. First request may take 30-60 seconds.

---

### **Option 3: Railway.app (Easy Deployment)**

#### Step 1: Create Railway Account
Sign up at: https://railway.app

#### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"** or **"Empty Project"**

#### Step 3: Add Service
1. Click **"+ New"** → **"GitHub Repo"** (or upload)
2. Select your repository
3. Railway auto-detects Dockerfile

#### Step 4: Configure Environment
- Railway will auto-deploy on every push
- Health checks are automatic

#### Step 5: Get Your URL
Railway provides: `https://your-app.railway.app`

**Flutter Integration:**
```dart
final url = 'https://your-app.railway.app/predict-emotion/';
```

---

### **Option 4: Docker + Local Network (For Testing on Same WiFi)**

#### Step 1: Build Docker Image
```bash
cd c:\Users\shadajifrin\Desktop\Projects\Facial-Expressions-Recognition-master\emotion_api
docker build -t emotion-api .
```

#### Step 2: Run Container
```bash
docker run -d -p 8000:8000 emotion-api
```

#### Step 3: Find Your Local IP
**Windows:**
```bash
ipconfig
```
Look for `IPv4 Address` (e.g., `192.168.1.100`)

#### Step 4: Use Local IP in Flutter
```dart
final url = 'http://192.168.1.100:8000/predict-emotion/';
```

**⚠️ Note:** Only works when mobile device is on the same WiFi network.

---

## 🔧 Flutter Integration Example

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

Future<Map<String, dynamic>> detectEmotion(File imageFile) async {
  final url = Uri.parse('YOUR_API_URL/predict-emotion/');
  
  var request = http.MultipartRequest('POST', url);
  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path)
  );
  
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  
  return json.decode(responseData);
}

// Usage
void main() async {
  File image = File('path/to/image.jpg');
  var result = await detectEmotion(image);
  
  if (result.containsKey('error')) {
    print('Error: ${result['error']}');
  } else {
    print('Emotion: ${result['emotion']}');
    print('Confidence: ${result['confidence']}');
  }
}
```

---

## 📊 Comparison

| Option | Cost | Setup Time | Stability | Best For |
|--------|------|------------|-----------|----------|
| **ngrok** | Free (temp URLs) | 2 min | Low | Quick testing |
| **Render.com** | Free | 10 min | High | Production (free) |
| **Railway.app** | Free tier | 10 min | High | Production |
| **Local Network** | Free | 5 min | Low | Testing on WiFi |

---

## 🎯 Recommended Path

1. **Start with ngrok** for immediate testing
2. **Deploy to Render.com** for permanent free hosting
3. **Use local network** for development without internet

---

## 🔒 Security Notes

1. **CORS is currently set to `*`** - Consider restricting to your Flutter app's domain in production
2. **No authentication** - Add API keys if needed
3. **File uploads** - Consider adding file size limits

---

## 🐛 Troubleshooting

### Issue: "No face detected"
- Ensure image has a clear, front-facing face
- Good lighting helps detection

### Issue: API timeout
- Render free tier spins down - first request takes longer
- Consider upgrading to paid tier for instant responses

### Issue: CORS errors in Flutter
- Already configured with `allow_origins=["*"]`
- For production, update to specific domains

---

## 📞 Support

For issues, check:
- FastAPI docs: https://fastapi.tiangolo.com
- Render docs: https://render.com/docs
- Railway docs: https://docs.railway.app
