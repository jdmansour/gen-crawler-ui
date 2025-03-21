FROM python:3.11-bookworm

WORKDIR /app/ui

RUN python -m pip install --upgrade pip
COPY requirements.txt /app/ui/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/ui

ENV DJANGO_VITE_DEV_MODE=False
CMD ["gunicorn", "crawler_ui.wsgi", "--bind", "0.0.0.0:8000"]