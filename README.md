# 🚀 ScrapeUnblocker - Bypass Anti-Bot Systems & Get Clean HTML

ScrapeUnblocker allows you to fetch the full HTML of almost any website - even those protected by advanced anti-bot systems.

Just provide a URL → get clean HTML.

---

## ⚡ Why use ScrapeUnblocker?

Most scraping tools fail on protected websites.

ScrapeUnblocker solves this by using real browser-like behavior and advanced bypass techniques.

* No browser setup
* No proxy setup
* No anti-bot headaches

---

## 🛠️ Features

* Fetch full HTML from protected websites
* Supports Cloudflare, PerimeterX, DataDome, Akamai
* Built-in rotating proxies
* Minimal input (only URL required)
* Returns raw HTML (NOT JSON-wrapped)

---

## 📥 Input

```json
{
  "url": "https://example.com"
}
```

---

## 📤 Output

Returns **raw HTML string** (not JSON):

```html
<html>...</html>
```

---

## 📊 Output schema (for Apify UI)

| Field | Type   | Description |
| ----- | ------ | ----------- |
| html  | string | Full HTML   |

---

## 🚀 How to use

### Python example

```python
import requests

API_TOKEN = "YOUR_APIFY_TOKEN"

response = requests.post(
    f"https://api.apify.com/v2/acts/scrapeunblocker~scrapeunblocker/run-sync?token={API_TOKEN}",
    json={"url": "https://example.com"}
)

html = response.text
print(html[:500])
```

---

### cURL example

```bash
curl -X POST "https://api.apify.com/v2/acts/scrapeunblocker~scrapeunblocker/run-sync?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' 
```

---

## 🔁 Real use cases

* Scraping marketplaces (cars, real estate, e-commerce)
* Extracting data from protected pages
* Feeding HTML into BeautifulSoup / Cheerio / LLMs
* Monitoring competitor pages

---

## ⚠️ Important notes

* Some websites may still require retries
* Response time depends on target protection level
* Works best for full-page HTML retrieval (not APIs)

---

## 💡 Pro tip

Need higher volume, better pricing, or full control?

👉 Use ScrapeUnblocker API directly instead of Apify