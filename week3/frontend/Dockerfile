# Build context must be the project root (ai-workbench/), since requirements.txt
# is shared across weeks and lives there. Compose already sets this; standalone:
#   docker build -f week3/frontend/Dockerfile -t ai-workbench-ui .
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY week3/frontend/streamlit_app.py .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
