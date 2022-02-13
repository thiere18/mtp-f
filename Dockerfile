FROM python:3.9.7

ENV HOME /app
WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip install poetry==1.1.12
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock /app/
RUN poetry install

COPY . .


EXPOSE 8000
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]