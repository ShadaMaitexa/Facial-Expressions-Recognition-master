# 🚀 Deploy Emotion Detection API (No ngrok)

## ✅ **Recommended: Render.com** (100% Free, Easiest)

### **Why Render.com?**
- ✅ **Completely FREE** forever
- ✅ Auto-deploys from GitHub
- ✅ HTTPS included automatically
- ✅ Perfect for Flutter mobile apps
- ✅ No credit card required

### **Steps to Deploy:**

#### **Step 1: Push to GitHub**

1. Create a new repository on GitHub: https://github.com/new
   - Name: `emotion-detection-api` (or any name)
   - Make it Public or Private (both work)

2. Copy the remote URL (e.g., `https://github.com/yourusername/emotion-detection-api.git`)

3. Run these commands in your terminal:

```bash
cd c:\Users\shadajifrin\Desktop\Projects\Facial-Expressions-Recognition-master

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### **Step 2: Deploy to Render**

1. Go to: https://render.com
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with GitHub (easiest)
4. Click **"New +"** → **"Web Service"**
5. Connect your GitHub repository
6. Configure:
   - **Name**: `emotion-detection-api`
   - **Root Directory**: `emotion_api`
   - **Runtime**: Docker
   - **Plan**: **FREE**
   - **Health Check Path**: `/`

7. Click **"Create Web Service"**

#### **Step 3: Wait for Deployment** (5-10 minutes)

Render will:
- Build your Docker image
- Deploy the API
- Give you a permanent URL

#### **Step 4: Get Your API URL**

You'll get a URL like: `https://emotion-detection-api-xyz.onrender.com`

### **Use in Flutter:**

```dart
final apiUrl = 'https://emotion-detection-api-xyz.onrender.com/predict-emotion/';
```

---

## 🏃 **Option 2: Railway.app** (Free $5/month credit)

### **Steps:**

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-detects the Dockerfile
6. Click **"Deploy"**

### **Get Your URL:**

Railway provides: `https://your-app.up.railway.app`

### **Use in Flutter:**

```dart
final apiUrl = 'https://your-app.up.railway.app/predict-emotion/';
```

---

## 🐍 **Option 3: PythonAnywhere** (Free Tier)

### **Steps:**

1. Sign up: https://www.pythonanywhere.com
2. Go to **"Web"** tab
3. Click **"Add a new web app"**
4. Choose **Manual configuration**
5. Upload your files via **"Files"** tab
6. Configure WSGI file for FastAPI
7. Install dependencies in Bash console

### **Your URL:**

`https://yourusername.pythonanywhere.com`

⚠️ **Note:** Requires manual setup, more complex than Render/Railway

---

## 📊 **Comparison**

| Platform | Free Plan | Setup Time | Best For | URL Stability |
|----------|-----------|------------|----------|---------------|
| **Render.com** | ✅ Unlimited | 10 min | Production | Excellent |
| **Railway.app** | ✅ $5/month credit | 10 min | Small projects | Excellent |
| **PythonAnywhere** | ✅ Limited | 30 min | Simple apps | Good |

---

## 🎯 **My Recommendation**

**Use Render.com** - It's the best free option for your use case:
- Zero configuration needed (Dockerfile detected automatically)
- Permanent free tier
- Professional URLs
- Perfect for Flutter mobile app integration

---

## 📱 **Flutter Integration Code**

Once deployed, use this in your Flutter app:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

class EmotionDetectionAPI {
  // Replace with your actual deployed URL
  static const String baseUrl = 'https://YOUR-APP-NAME.onrender.com';
  
  static Future<Map<String, dynamic>> detectEmotion(File imageFile) async {
    try {
      final url = Uri.parse('$baseUrl/predict-emotion/');
      
      var request = http.MultipartRequest('POST', url);
      request.files.add(
        await http.MultipartFile.fromPath('file', imageFile.path)
      );
      
      var response = await request.send();
      var responseData = await response.stream.bytesToString();
      
      return json.decode(responseData);
    } catch (e) {
      return {'error': 'Failed to connect to API: $e'};
    }
  }
}

// Usage Example
void main() async {
  File image = File('path/to/image.jpg');
  var result = await EmotionDetectionAPI.detectEmotion(image);
  
  if (result.containsKey('error')) {
    print('Error: ${result['error']}');
  } else {
    print('Emotion: ${result['emotion']}');
    print('Confidence: ${(result['confidence'] * 100).toStringAsFixed(2)}%');
  }
}
```

---

## ⚠️ **Important Notes**

### **Render.com Free Tier:**
- ✅ Unlimited hours
- ⚠️ Spins down after 15 minutes of inactivity
- ⏱️ First request after spindown: 30-60 seconds to wake up
- 💡 Subsequent requests: instant

### **To avoid spindown:**
- Upgrade to paid tier ($7/month) for always-on
- OR use a cron job to ping your API every 10 minutes

### **Loading State in Flutter:**

```dart
Future<void> callAPI() async {
  setState(() => isLoading = true);
  
  // Show message if taking too long
  Timer(Duration(seconds: 5), () {
    if (isLoading) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('API is waking up, please wait...'))
      );
    }
  });
  
  var result = await EmotionDetectionAPI.detectEmotion(imageFile);
  
  setState(() => isLoading = false);
}
```

---

## 🔧 **Testing Your Deployed API**

Once deployed, test it:

```bash
# Replace with your actual URL
curl -X POST "https://your-app.onrender.com/predict-emotion/" \
  -F "file=@path/to/your/image.jpg"
```

Or visit: `https://your-app.onrender.com` in browser to see the web UI

---

## 🐛 **Troubleshooting**

### **Build Failed on Render:**
- Check build logs in Render dashboard
- Ensure `emotion_api` folder has all required files
- Verify Dockerfile is correct

### **API Returns 500 Error:**
- Check Render logs for Python errors
- Ensure model file (`Emotion_little_vgg.h5`) is uploaded
- Verify haarcascade XML file is present

### **Flutter Can't Connect:**
- Check CORS settings (already configured for `*`)
- Ensure you're using HTTPS URL
- Test API directly in browser first

---

## 📞 **Next Steps**

1. ✅ Push code to GitHub (already done!)
2. 🌐 Create Render.com account
3. 🚀 Deploy from GitHub
4. 📱 Update Flutter app with your new URL
5. 🎉 Test and enjoy!

---

**Need help?** Let me know which platform you choose!
