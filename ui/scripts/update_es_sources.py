import os
import random
import sys
from pathlib import Path
import django
django_root = Path(__file__).resolve().parents[1]
sys.path.append(str(django_root))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler_ui.settings")
django.setup()


from crawls.models import SourceItem
import json

def main():
    with open('data/es_sources_dump.json', 'r') as f:
        data = json.load(f)

    for item in data['nodes']:
        # TODO: in edu-sharing, there can be multiple repos. This just assumes
        # we are working with the home repo.
        guid = item['ref']['id']
        title = item['title']
        source_item, created = SourceItem.objects.get_or_create(
            guid=guid,
            defaults={
                'title': title,
                'data': item,
            }
        )
        if created:
            print(f"Created SourceItem: {source_item}")
        else:
            print(f"SourceItem already exists: {source_item}")
    

if __name__ == "__main__":
    main()