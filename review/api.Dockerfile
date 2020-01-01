# pull official base image
FROM python:3.6.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/

# to prevent poetry from installing my actual app,
# and keep docker able to cache layers
RUN mkdir -p /app/src/app
RUN touch /app/src/app/__init__.py

RUN poetry install -n --no-dev

# now actually copy the real contents of my app
COPY . .
RUN touch .env

EXPOSE 8000

CMD ["gunicorn", "review.wsgi:application", "--bind", "0.0.0.0:8000"]
