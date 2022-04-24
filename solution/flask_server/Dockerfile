FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano vim
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /var/www/requirements.txt
