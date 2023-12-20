FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py ./planner1_src/
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8100
CMD ["python", "./planner1_src/main.py"]
