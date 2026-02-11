# Use a lightweight Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model and cascade files (they are in the same directory as app.py)
COPY Emotion_little_vgg.h5 .
COPY haarcascade_frontalface_default.xml .
COPY model_loader.py .
COPY app.py .

# Create uploads directory
RUN mkdir -p uploads

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
