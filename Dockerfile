FROM python:3.11

WORKDIR /app

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["streamlit", "run", "app/main.py", "--server.port=8000", "--server.address=0.0.0.0"]

