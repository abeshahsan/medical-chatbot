FROM python:3.10-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

RUN pip install gunicorn==22.0.0
RUN pip install torch==2.5.0 --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt

# Copy rest of the code
COPY . .

RUN pip install .

EXPOSE 5000


CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]