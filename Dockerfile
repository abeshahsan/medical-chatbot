FROM python:3.10-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

RUN pip install torch==2.5.0 --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt

# Copy rest of the code
COPY . .

RUN pip install .

# Expose port (change if needed)
EXPOSE 5000

# Run your app (adjust to your framework)
CMD ["python", "app.py"]