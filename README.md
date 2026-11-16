# IR Lab 5 — bookcrawler

Scrapy project for IR 2026 Lab 5. It crawls a bounded sample of
[Books to Scrape](https://books.toscrape.com/), a sandbox site built for scraping practice.

## What it does

- `parse()` reads a listing page, follows every book card to its detail page,
  then follows `li.next a`, stopping after `max_pages` listing pages (1 or 2).
- `parse_book()` yields one `BookItem` per book: `doc_id`, `title`, `text`,
  `description`, `url`, `category`, `price_gbp`, `rating`, `availability`, `source`.
  `doc_id` is the first 12 hex characters of `sha1(url)`.
- `CorpusQualityPipeline` drops records with no title or a repeated `doc_id`.
- Polite settings: `ROBOTSTXT_OBEY = True`, one request at a time,
  `DOWNLOAD_DELAY = 0.5`, `DOWNLOAD_TIMEOUT = 20`, retries on 429/5xx.

## Run

```bash
pip install "Scrapy>=2.11,<3"
scrapy crawl books -a max_pages=1 -O books_scrapy_preview.json
scrapy crawl books -a max_pages=2 -O books_scrapy.json -O books_scrapy.csv
```

## Output

| File | Records |
|---|---|
| `books_scrapy_preview.json` | 20 (1 listing page) |
| `books_scrapy.json` / `books_scrapy.csv` | 40 (2 listing pages) |
