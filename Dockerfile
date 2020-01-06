FROM python:2-alpine

RUN apk add --no-cache git

# Create app directory
WORKDIR /usr/src/app

# Install requirements.
COPY requirements.pip ./
RUN pip install -r requirements.pip

# Bundle app source afterwards, to ensure that file changes don't
# force us to reinstall.
COPY . .

RUN python manage.py collectstatic --noinput && python manage.py syncdb
COPY picky/live_settings_example.py picky/live_settings.py

EXPOSE 9001
# Loosely based on https://pythonspeed.com/articles/gunicorn-in-docker/
CMD ["gunicorn", "wsgi", "--worker-tmp-dir=/dev/shm", "-b", "0.0.0.0:9001", "--log-file=-", "--workers=2"]
