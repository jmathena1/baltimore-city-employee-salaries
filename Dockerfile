FROM python:3.11-slim-bookworm
ARG PORT=8080
WORKDIR /home
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]