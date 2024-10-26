###########
# BUILDER #
###########

# pull official base image
FROM python:3.12-bookworm AS builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip poetry poetry-plugin-export

COPY ./app/pyproject.toml .

# install python dependencies
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with postgres --with mysql
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.12-bookworm

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $HOME/static
RUN mkdir $HOME/media
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY app $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME
RUN chown -R app:app $HOME/static
RUN chown -R app:app $HOME/media

# change to the app user
USER app

EXPOSE 8000

ENTRYPOINT ["gunicorn"]