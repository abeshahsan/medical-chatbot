

echo "Installing dependencies..."
pip install -r requirements.txt
if errorlevel 1 exit /b 1
pip install -r requirements-dev.txt
if errorlevel 1 exit /b 1

echo "Running tests..."
REM replace with actual tests later
echo "No tests yet"

echo "Building Docker image..."
docker build -t rag-backend .
if errorlevel 1 exit /b 1

echo "Running container..."
docker run -d -p 5000:5000 --name rag-app rag-backend
echo "✅ Pipeline complete!"