
import trafilatura

from .metadata_enricher import MetadataEnricher

SAMPLE_DOCUMENT = """
<html lang="de">
<head>
<title>Page title</title>
</head>
<body>
<p>Some content</p>
</body>
</html>
"""


async def test_extract_title():
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


async def test_empty_keywords():
    enricher = MetadataEnricher(ai_enabled=False)
    settings = {}
    enricher.setup(settings)

    html = SAMPLE_DOCUMENT
    html_bytes: bytes = html.encode()
    trafilatura_text: str = trafilatura.extract(html_bytes) or ""

    response_url = "https://example.com"
    item = await enricher.parse_page_inner(response_url, html, trafilatura_text)
    keywords = item['lom']['general'].get('keyword', [])
    assert keywords == []


async def test_extract_language():
    enricher = MetadataEnricher(ai_enabled=False)
    settings = {}
    enricher.setup(settings)

    html = SAMPLE_DOCUMENT
    html_bytes: bytes = html.encode()
    trafilatura_text: str = trafilatura.extract(html_bytes) or ""

    response_url = "https://example.com"
    item = await enricher.parse_page_inner(response_url, html, trafilatura_text)
    languages = item['lom']['general']['language']
    assert languages == ["de"]


JSONLD_VIDEO_DOCUMENT = """
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


async def test_jsonld_video():
    """ Check if we can detect a JSON-LD VideoObject and extract the relevant metadata. """
    # Example URL: https://diler.tube/w/jjputb5r2zDH1bKXCVxLpu

    enricher = MetadataEnricher(ai_enabled=False)
    settings = {}
    enricher.setup(settings)

    html = JSONLD_VIDEO_DOCUMENT
    html_bytes: bytes = html.encode()
    trafilatura_text: str = trafilatura.extract(html_bytes) or ""
    response_url = "https://example.com"
    item = await enricher.parse_page_inner(response_url, html, trafilatura_text)

    LRT_VIDEO = "http://w3id.org/openeduhub/vocabs/learningResourceType/video"
    assert item['valuespaces']['learningResourceType'][0] == LRT_VIDEO
    # duration is in seconds here
    assert item['lom']['technical']['duration'] == 189


META_TAGS_DOCUMENT = """
<html lang="de">
<head>
<title>Page title</title>
<meta name="keywords" content="keyword1, keyword2, keyword3">
<meta name="description" content="This is a sample description.">
</head>
<body>
<p>Some content</p>
</body>
</html>
"""


async def test_reads_keywords_from_meta():
    enricher = MetadataEnricher(ai_enabled=False)
    settings = {}
    enricher.setup(settings)

    html = META_TAGS_DOCUMENT
    html_bytes: bytes = html.encode()
    trafilatura_text: str = trafilatura.extract(html_bytes) or ""

    response_url = "https://example.com"
    item = await enricher.parse_page_inner(response_url, html, trafilatura_text)

    assert item['lom']['general']['keyword'] == [
        "keyword1", "keyword2", "keyword3"]


async def test_reads_description_from_meta():
    enricher = MetadataEnricher(ai_enabled=False)
    settings = {}
    enricher.setup(settings)

    html = META_TAGS_DOCUMENT
    html_bytes: bytes = html.encode()
    trafilatura_text: str = trafilatura.extract(html_bytes) or ""

    response_url = "https://example.com"
    item = await enricher.parse_page_inner(response_url, html, trafilatura_text)

    assert item['lom']['general']['description'] == "This is a sample description."


JSONLD_ARTICLE_DOCUMENT = """
<html lang="de">
<head>
<title>Page title</title>
<script type="application/ld+json">{
    "@context": "https:\\/\\/schema.org",
    "@type": "Article",
    "author": "Bundeszentrale f\\u00fcr politische Bildung",
    "headline": "Pr\\u00e4sidentschaftswahl in Portugal | Hintergrund aktuell | bpb.de",
    "datePublished": "2026-01-20",
    "dateCreated": "2026-01-13",
    "dateModified": "2026-01-20",
    "mainEntityOfPage": "https:\\/\\/www.bpb.de\\/kurz-knapp\\/hintergrund-aktuell\\/574401\\/praesidentschaftswahl-in-portugal\\/",
    "description": "Ant\\u00f3nio Jos\\u00e9 Seguro (Partido Socialista) hat die erste Runde der Pr\\u00e4sidentschaftswahl in Portugal gewonnen und tritt in der Stichwahl am achten Februar gegen den Kandidaten der rechtspopulistischen Chega an.",
    "keywords": "Portugal,Wahl,Staatsoberhaupt,Pr\\u00e4sidentschaftswahl,Stichwahl,Minderheitsregierung",
    "publisher": {
        "@type": "Organization",
        "name": "Bundeszentrale f\\u00fcr politische Bildung",
        "logo": {
            "@type": "ImageObject",
            "url": "https:\\/\\/www.bpb.de\\/themes\\/custom\\/bpbtheme\\/images\\/bpb_logo_ldjson.jpg",
            "width": "144",
            "height": "60"
        }
    },
    "image": {
        "@type": "ImageObject",
        "url": "https:\\/\\/www.bpb.de\\/cache\\/images\\/8\\/796658_teaser_3x2_800.jpg?8D58B",
        "width": 800,
        "height": 534
    }
}</script></head>
<body>
<p>Some content</p>
</body>
</html>
"""


async def test_jsonld_article_keywords():
    enricher = MetadataEnricher(ai_enabled=False)
    settings = {}
    enricher.setup(settings)

    html = JSONLD_ARTICLE_DOCUMENT
    html_bytes: bytes = html.encode()
    trafilatura_text: str = trafilatura.extract(html_bytes) or ""
    response_url = "https://example.com"
    item = await enricher.parse_page_inner(response_url, html, trafilatura_text)

    assert item['lom']['general']['keyword'] == ["Portugal", "Wahl",
                                                 "Staatsoberhaupt", "Präsidentschaftswahl", "Stichwahl", "Minderheitsregierung"]


PLANET_SCHULE_VIDEO_DOCUMENT = """
<html lang="de">
<head>
<title>Page title</title>
<meta name="planet-schule:schoolsubjects" content="geschichte[Geschichte],medienkompetenz[Medienkompetenz],religion_ethik[Religion / Ethik],sachunterricht[Sachunterricht]">
<meta name="planet-schule:schoolclasses" content="klasse04[4. Klasse],klasse05[5. Klasse],klasse06[6. Klasse],klasse07[7. Klasse],klasse08[8. Klasse],klasse09[9. Klasse],klasse10[10. Klasse]">
<meta name="planet-schule:mediatypes" content="video[Video]">
</head>
<body>
<p>Some content</p>
</body>
</html>
"""


async def test_planet_schule_video():
    """ Check if we can detect a video based on the planet-schule:mediatypes meta tag. """

    enricher = MetadataEnricher(ai_enabled=False)
    settings = {}
    enricher.setup(settings)

    html = PLANET_SCHULE_VIDEO_DOCUMENT
    html_bytes: bytes = html.encode()
    trafilatura_text: str = trafilatura.extract(html_bytes) or ""
    response_url = "https://example.com"
    item = await enricher.parse_page_inner(response_url, html, trafilatura_text)

    LRT_VIDEO = "http://w3id.org/openeduhub/vocabs/learningResourceType/video"
    assert item['valuespaces']['learningResourceType'][0] == LRT_VIDEO
