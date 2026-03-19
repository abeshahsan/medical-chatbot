#!/bin/bash

echo "🔧 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

echo "🧪 Running tests..."
# replace with actual tests later
echo "No tests yet"

echo "🐳 Building Docker image..."
docker build -t rag-backend .

echo "🚀 Running container..."
docker run -d -p 5000:5000 --name rag-app rag-backend
echo "✅ Pipeline complete!"