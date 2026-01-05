FROM python:3.12.2-slim
WORKDIR /app
COPY app/ .
RUN apt-get update && apt-get install -y curl
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
