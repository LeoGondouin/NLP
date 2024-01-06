FROM python:3.8-slim

WORKDIR /api/scrapper

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001  # Expose a different port for fastapi1

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]