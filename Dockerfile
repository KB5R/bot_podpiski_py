FROM python:3.13.1-slim
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
