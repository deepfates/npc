FROM python:3.9

COPY pyproject.toml /app/
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install poetry

RUN cd /app && poetry config virtualenvs.create false && poetry install --no-dev
COPY . /app

WORKDIR /app
CMD ["poetry", "run", "python", "server.py"]
