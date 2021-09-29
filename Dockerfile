FROM python:3.10.0b4

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN python manage.py makemigrations app
RUN python manage.py sqlmigrate app 0001
RUN python manage.py migrate

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "idVerification.wsgi:application" ]
