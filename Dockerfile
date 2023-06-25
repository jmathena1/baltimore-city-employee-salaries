FROM python:3.11-slim-bookworm
WORKDIR /home
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "get-baltimore-city-salaries.py"]