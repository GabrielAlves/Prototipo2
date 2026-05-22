FROM python:3.11-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV BACKEND_API_BASE 'http://localhost:8001'

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]