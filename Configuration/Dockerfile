FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py ./config_src/
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8120
CMD ["python", "./config_src/main.py"]
