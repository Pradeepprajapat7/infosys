# 1. Start with a Python system
FROM python:3.9-slim

# 2. Set the folder inside the container
WORKDIR /app

# 3. Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your code and model
COPY . .

# 5. command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]