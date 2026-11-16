# Schema of one scraped book record (one IR document).
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class BookItem:
    doc_id: str                      # stable id: first 12 hex chars of sha1(url)
    title: str
    text: str                        # title + description, used for indexing
    description: str                 # "" when the book has no description
    url: str
    category: str | None = None
    price_gbp: float | None = None
    rating: int | None = None        # 1..5
    availability: str | None = None
    source: str = "https://books.toscrape.com/"
