
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