FROM gomonuk/pythonbase:latest

WORKDIR /usr/src/app/
COPY src poetry.lock pyproject.toml .env /usr/src/app/
RUN poetry install --no-dev --no-interaction --no-ansi
CMD ["python", "main.py"]
