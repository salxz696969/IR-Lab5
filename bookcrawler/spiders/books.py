import hashlib
import re

import scrapy

from bookcrawler.items import BookItem

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
SOURCE = "https://books.toscrape.com/"


def clean(text):
    """Collapse runs of whitespace; return "" for None."""
    return " ".join((text or "").split())


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [SOURCE]

    def __init__(self, max_pages=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lab boundary: at least 1 and at most 2 listing pages.
        self.max_pages = min(2, max(1, int(max_pages)))
        self.pages_seen = 0

    # ---- listing pages -------------------------------------------------
    def parse(self, response):
        self.pages_seen += 1
        self.logger.info("Listing page %d/%d: %s",
                         self.pages_seen, self.max_pages, response.url)

        # One detail request per book card.
        for href in response.css("article.product_pod h3 a::attr(href)").getall():
            yield response.follow(href, callback=self.parse_book)

        # Next listing page, only while we are under the page limit.
        next_href = response.css("li.next a::attr(href)").get()
        if next_href and self.pages_seen < self.max_pages:
            yield response.follow(next_href, callback=self.parse)

    # ---- book detail pages ---------------------------------------------
    def parse_book(self, response):
        main = response.css("div.product_main")

        title = clean(main.css("h1::text").get())

        # " ::text" (with the space) already includes the paragraph's own
        # text, so selecting "p::text" as well would duplicate it.
        description = clean(" ".join(
            response.css("#product_description + p ::text").getall()))

        category = clean(response.css(
            "ul.breadcrumb li:nth-child(3) a::text").get()) or None

        price_match = re.search(r"\d+(?:\.\d+)?",
                                main.css("p.price_color::text").get(default=""))
        price_gbp = float(price_match.group()) if price_match else None

        star_classes = main.css("p.star-rating::attr(class)").get(default="").split()
        rating = next((RATINGS[c] for c in star_classes if c in RATINGS), None)

        availability = clean(" ".join(
            main.css("p.availability ::text").getall())) or None

        yield BookItem(
            doc_id=hashlib.sha1(response.url.encode("utf-8")).hexdigest()[:12],
            title=title,
            text=f"{title} {description}".strip(),
            description=description,
            url=response.url,
            category=category,
            price_gbp=price_gbp,
            rating=rating,
            availability=availability,
            source=SOURCE,
        )
