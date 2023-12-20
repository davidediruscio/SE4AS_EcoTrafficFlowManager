FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py ./monitor_src/
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "./monitor_src/main.py"]
