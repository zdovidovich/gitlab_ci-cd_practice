FROM python:3.14.5-alpine3.23

LABEL author=zdovidovich

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN adduser -S web_user && chown web_user /app

COPY --chown=web_user . .

EXPOSE 8000

USER web_user

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]