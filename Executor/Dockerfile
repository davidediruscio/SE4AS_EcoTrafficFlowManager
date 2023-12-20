FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py ./executor_src/
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8120
CMD ["python", "./executor_src/main.py"]
