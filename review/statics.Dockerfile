FROM nginx:1.16-alpine

COPY ./staticfiles/ /usr/share/nginx/html/django-statics

EXPOSE 80
