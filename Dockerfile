FROM  python:3.12-slim

WORKDIR crm/

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-root

COPY . ./

RUN chmod +x ./start_app.sh
CMD ["./start_app.sh"]