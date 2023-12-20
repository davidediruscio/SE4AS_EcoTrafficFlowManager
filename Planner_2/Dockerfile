FROM python:3.10-slim
LABEL authors="sea4as"

COPY *.py ./planner2_src/
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8110
CMD ["python", "./planner2_src/main.py"]
