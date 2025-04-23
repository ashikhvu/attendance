FROM python:3.13-slim

RUN apt-get update && apt-get install -y libzbar0

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["gunicorn", "project_attendance.wsgi:application", "--bind", "0.0.0.0:8000"]