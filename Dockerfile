FROM tiangolo/uwsgi-nginx-flask:python3.7


RUN pip3 install requests flask-cors

ENV LISTEN_PORT 8080
EXPOSE 8080

COPY ./app /app