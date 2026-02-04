FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN pip install --no-cache-dir uv \
    && uv sync --frozen

COPY . .

CMD ["uv","run","gunicorn","app.main:app" , "-k","uvicorn.workers.UvicornWorker","-w","2","-b","0.0.0.0:8000"]

