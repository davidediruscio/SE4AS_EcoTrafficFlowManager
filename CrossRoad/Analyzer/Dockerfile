FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py .
COPY requirements.txt .
COPY car.xml .
RUN pip install -r requirements.txt

EXPOSE 8090
CMD ["python", "./main.py"]
