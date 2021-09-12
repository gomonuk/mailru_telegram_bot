FROM gomonuk/pythonbase:latest

WORKDIR /usr/src/app/
COPY src poetry.lock pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi
CMD ["python", "main.py"]
