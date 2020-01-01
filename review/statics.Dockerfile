FROM nginx:1.16-alpine

COPY ./django-statics/ /usr/share/nginx/html/django-statics

EXPOSE 80
