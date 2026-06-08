# 🚀 ScrapeUnblocker - Bypass Anti-Bot Systems & Get Clean HTML or Parsed JSON

**ScrapeUnblocker is the most advanced tool on the market, capable of defeating the most complex protections and anti-bot systems.** It fetches the full HTML of almost any website effortlessly — and can now return **ready-to-use structured JSON** instead of raw HTML.

Just provide a URL → get clean HTML, or flip one switch → get **parsed data** extracted for you.

---

## ⚡ Why use ScrapeUnblocker?

Most scraping tools fail on protected websites.

ScrapeUnblocker solves this by using real browser-like behavior and advanced bypass techniques.

* No browser setup
* No proxy setup
* No anti-bot headaches

---

## ✨ NEW: Get parsed data instantly (`parsed_data`)

Stop writing brittle HTML parsers. Set `parsed_data: true` and ScrapeUnblocker returns **clean structured JSON** — titles, prices, listings, key fields — extracted straight from the page via Schema.org / `__NEXT_DATA__` / AI-generated rules.

* 🧠 **Skip the parsing work** — get usable JSON, not a 1 MB HTML blob
* 🤖 **AI-powered extraction** that adapts per page type
* 🔁 **One input flag** — `parsed_data: true`, nothing else to set up

This is a genuine superpower: bypass the anti-bot **and** the data is already structured for you.

---

## 🛠️ Features

* Fetch full HTML from protected websites
* **Optional parsed JSON output** (`parsed_data: true`)
* Supports Cloudflare, PerimeterX, DataDome, Akamai
* Built-in rotating proxies
* Minimal input (only URL required)

---

## 📥 Input

Raw HTML (default):

```json
{
  "url": "https://example.com"
}
```

Parsed structured JSON:

```json
{
  "url": "https://example.com",
  "parsed_data": true
}
```

---

## 📤 Output

**Default (`parsed_data: false`)** — one dataset item with the full HTML:

```json
{
  "url": "https://example.com",
  "html": "<html>...</html>"
}
```

**With `parsed_data: true`** — one dataset item with structured JSON (shape depends on the page type):

```json
{
  "url": "https://autoplius.lt/skelbimai/naudoti-automobiliai",
  "page_type": "search_list",
  "data": {
    "results": {
      "items": [
        { "title": "BMW i5 2024 ...", "url": "https://autoplius.lt/skelbimai/..." }
      ]
    }
  },
  "source": "ai-rules"
}
```

---

## 🚀 How to use

### Python example

```python
import requests

API_TOKEN = "YOUR_APIFY_TOKEN"

response = requests.post(
    f"https://api.apify.com/v2/acts/scrapeunblocker~scrapeunblocker/run-sync-get-dataset-items?token={API_TOKEN}",
    json={"url": "https://example.com", "parsed_data": True}
)

print(response.json())
```

---

### cURL example

```bash
curl -X POST "https://api.apify.com/v2/acts/scrapeunblocker~scrapeunblocker/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "parsed_data": true}'
```

---

## 🔁 Real use cases

* Scraping marketplaces (cars, real estate, e-commerce)
* Extracting **structured data** from protected pages without writing parsers
* Feeding HTML into BeautifulSoup / Cheerio / LLMs
* Monitoring competitor pages

---

## ⚠️ Important notes

* **Retries are expected:** Due to the nature of complex anti-bot systems, requests might not always succeed on the first try and you may encounter errors. If a request fails, we highly recommend trying again, as subsequent attempts are often successful.
* When `parsed_data: true` is used on a brand-new domain, extraction rules may still be generating — the Actor automatically waits and retries until the parsed result is ready.
* Response time depends on target protection level

---

## 💡 More tools, docs & functionality

ScrapeUnblocker also offers SERP scraping, image fetching, cookies retrieval and more.

👉 Explore the full documentation and feature set at **[scrapeunblocker.com](https://www.scrapeunblocker.com/)**
