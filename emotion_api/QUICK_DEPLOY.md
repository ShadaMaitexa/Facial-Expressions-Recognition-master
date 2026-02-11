# Quick Deploy Commands

## Step 1: Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `emotion-detection-api`
3. Make it Public
4. Click "Create repository"
5. Copy the repository URL

## Step 2: Push to GitHub

Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values:

```powershell
cd c:\Users\shadajifrin\Desktop\Projects\Facial-Expressions-Recognition-master

# Add remote (replace with YOUR GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Render.com

1. Go to: https://render.com
2. Sign up (use GitHub login - easiest)
3. Click "New +" → "Web Service"
4. Select your repository
5. Settings:
   - **Name**: emotion-detection-api
   - **Root Directory**: `emotion_api`
   - **Environment**: Docker
   - **Plan**: Free
6. Click "Create Web Service"

## Step 4: Wait 5-10 Minutes

Render will build and deploy your API automatically!

## Step 5: Get Your URL

You'll get: `https://emotion-detection-api-XXXX.onrender.com`

## Step 6: Update Flutter App

```dart
final apiUrl = 'https://YOUR-APP.onrender.com/predict-emotion/';
```

Done! 🎉
