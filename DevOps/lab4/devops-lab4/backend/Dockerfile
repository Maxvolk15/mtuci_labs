FROM python:3.10
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt
WORKDIR /app
COPY src .
CMD ["python", "main.py"]