# Item pipeline: last quality gate before records reach the JSON/CSV export.
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CorpusQualityPipeline:
    """Drop records with no title and records already seen (same doc_id)."""

    def __init__(self):
        self.seen_ids = set()

    def process_item(self, item):
        adapter = ItemAdapter(item)

        if not adapter.get("title"):
            raise DropItem(f"Missing title: {adapter.get('url')}")

        doc_id = adapter.get("doc_id")
        if doc_id in self.seen_ids:
            raise DropItem(f"Duplicate doc_id {doc_id}: {adapter.get('url')}")
        self.seen_ids.add(doc_id)

        return item
