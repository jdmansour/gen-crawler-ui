
# First stage: build the egg file

FROM python as build-stage

RUN pip install --no-cache-dir scrapyd-client
WORKDIR /workdir
COPY . .
RUN scrapyd-deploy --build-egg=generic_crawler.egg

# Main stage: build the scrapyd container

FROM python:alpine

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir scrapyd && \
    pip install --no-cache-dir -r requirements.txt
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
COPY ./scrapyd.conf /etc/scrapyd/
RUN mkdir -p /app/eggs
# The name of the project is "scraper"
COPY --from=build-stage /workdir/generic_crawler.egg /app/eggs/scraper/1_0.egg
EXPOSE 6800
ENV DB_PATH=/app/database/db.sqlite
# We have to mount /app/database in the docker compose file.
CMD ["scrapyd", "--pidfile="]