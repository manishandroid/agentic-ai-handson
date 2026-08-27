# Build context must be the project root (ai-workbench/), since requirements.txt
# is shared across weeks and lives there:
#   docker build -f week3/backend/Dockerfile -t ai-workbench-api .
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY week3/backend/app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
