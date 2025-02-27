FROM python:3.11-slim-bookworm

WORKDIR /app

RUN python -m pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENV DJANGO_VITE_DEV_MODE=False
CMD ["gunicorn", "crawler_ui.wsgi", "--bind", "0.0.0.0:8000"]