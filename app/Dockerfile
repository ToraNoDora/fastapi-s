FROM python:3.8

RUN addgroup --system app && adduser --system --group app

RUN apt-get update && apt-get install -y \
    curl

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

ARG INSTALL_DEV=false

RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . /app
RUN chmod +x run.sh

ENV PYTHONPATH=/app

RUN chown -R app:app $HOME


CMD ["./run.sh"]
