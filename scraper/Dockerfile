
# First stage: build the egg file

FROM python AS build-stage

RUN pip install --no-cache-dir scrapyd-client
WORKDIR /workdir
COPY . .
RUN scrapyd-deploy --build-egg=generic_crawler.egg

# Main stage: build the scrapyd container

# FROM --platform=linux/amd64 python:alpine
FROM --platform=linux/amd64 python:3.12

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir scrapyd regex && \
    pip install --no-cache-dir -r requirements.txt
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
COPY ./scrapyd.conf /etc/scrapyd/
RUN mkdir -p /app/eggs
# The name of the project is "scraper"
COPY --from=build-stage /workdir/generic_crawler.egg /app/eggs/scraper/1_0.egg
EXPOSE 6800
ENV DB_PATH=/app/database/db.sqlite
# RUN pip install regex scrapy overrides==3.1.0 pillow python-dotenv httpx vobject html2text trafilatura greenlet scrapyd scrapyd-client
RUN pip install regex scrapy overrides pillow python-dotenv httpx vobject html2text trafilatura greenlet scrapyd scrapyd-client playwright isodate langcodes extruct==0.16.0 lxml==5.1.0 async-lru xmltodict openai
#COPY ../oeh-valuespace_converter/ valuespace_converter/

# We have to mount /app/database in the docker compose file.
CMD ["scrapyd", "--pidfile="]
#CMD ["uname", "-a"]