FROM python:3.10.12
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
RUN mkdir app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . /app/
WORKDIR /app
RUN mkdir plots
RUN python manage.py collectstatic --noinput
RUN chmod +x start_celery.sh
