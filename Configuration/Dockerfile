FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py .
COPY config.json .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8120
CMD ["python", "./main.py"]
