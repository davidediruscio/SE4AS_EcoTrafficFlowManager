FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py ./analyzer_src/
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8090
CMD ["python", "./analyzer_src/main.py"]
