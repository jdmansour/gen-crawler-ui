
import asyncio

import trafilatura
from rich.pretty import pprint
from scrapy.item import Item

from metadataenricher.metadata_enricher import MetadataEnricher

SAMPLE_DOCUMENT = """
<html lang="de">
<head>
<title>Page title</title>
<script type="application/ld+json">{"@context":"http://schema.org","@type":"VideoObject","name":"Algeria in a Nutshell","description":"Algerien, als mittleres der Maghrebländer, ist der Fläche nach der größte Staat des afrikanischen Kontinents und der zehntgrößte Staat der Welt. Nach Einwohnern lag Algerien im Jahr 2017 innerhalb ...","image":"https://diler.tube/lazy-static/previews/26ce5904-0a04-4c52-80d0-551c6372bcb4.jpg","url":"https://diler.tube/w/jjputb5r2zDH1bKXCVxLpu","embedUrl":"https://diler.tube/videos/embed/94565c48-8e58-47a1-b022-7c2fa8de126a","uploadDate":"2024-07-09T02:38:13.796Z","duration":"PT189S","thumbnailUrl":"https://diler.tube/lazy-static/previews/26ce5904-0a04-4c52-80d0-551c6372bcb4.jpg"}</script>
</head>
<body>
<p>Some content</p>
</body>
</html>
"""


async def main():
    enricher = MetadataEnricher(ai_enabled=False)
    settings = {}
    enricher.setup(settings)

    html = SAMPLE_DOCUMENT
    html_bytes: bytes = html.encode()
    trafilatura_text: str = trafilatura.extract(html_bytes) or ""

    response_url = "https://example.com"
    item = await enricher.parse_page_inner(response_url, html, trafilatura_text)
    title = item['lom']['general']['title']
    assert title == "Page title"
    print(type(item))
    pprint(to_dict(item))


def to_dict(item: Item) -> dict:
    # convert to dict, including nested items
    if isinstance(item, Item):
        return {k: to_dict(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [to_dict(i) for i in item]
    else:
        return item


if __name__ == "__main__":
    asyncio.run(main())
