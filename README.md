# Performance Review

## Development
- Install [pyenv](https://github.com/pyenv/pyenv#the-automatic-installer)
- Install python 3.6.9 `pyenv install 3.6.9`
- Create python virtual environment named pr `pyenv virtualenv 3.6.9 pr`
- Install [poetry](https://github.com/sdispater/poetry#installation)
- Install dependencies `poetry install`
- Create `.env` based on the given `sample.env` in root and in `docker/development`
- Run docker compose file at `docker/development` to create PostgreSQL container `docker-compose up`
