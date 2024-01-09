FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8110
CMD ["python", "./main.py"]
