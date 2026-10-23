# 🚀 ScrapeUnblocker - Bypass Anti-Bot Systems & Get Clean HTML, Markdown or Parsed JSON

**ScrapeUnblocker is the most advanced tool on the market, capable of defeating the most complex protections and anti-bot systems.** It fetches the full HTML of almost any website effortlessly — and can now return **ready-to-use structured JSON** instead of raw HTML.

Just provide a URL → get clean HTML, or flip one switch → get **parsed data** extracted for you, or the page as **clean Markdown** for your LLM.

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

## 📝 NEW: Get the page as Markdown for LLMs (`markdown`)

Set `markdown: true` and the Actor returns the page as **clean Markdown** instead of HTML: headings, lists, tables, absolute links, images with their alt text and code blocks, without scripts, styles, navigation, footers, forms or hidden elements. It is built for LLMs, AI agents and RAG pipelines: no HTML cleanup on your side, and the Markdown is usually a small fraction of the HTML's size, so it costs far fewer tokens.

* 🎯 **Main content only by default** - navigation, the site header, footer and sidebars are dropped (`main_content_only: true`). Set `main_content_only: false` to convert the whole page.
* 🔁 Works with `proxy_country` and `steps`, and is charged like an HTML result.
* `markdown` cannot be combined with `parsed_data` or `list_elements`, which return their own JSON formats.

```json
{
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "markdown": true
}
```

Returns one dataset item:

```json
{
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "markdown": "...\n\n# A Light in the Attic\n\n£51.77\n\nIn stock (22 available)\n\n..."
}
```

---

## 🛠️ Features

* Fetch full HTML from protected websites
* **Optional parsed JSON output** (`parsed_data: true`)
* **Clean Markdown output** for LLMs, AI agents and RAG (`markdown: true`)
* **Browser steps** — click, type, select, scroll, wait for elements before capturing the page (`steps`)
* **Discover interactive elements** with ready-to-use selectors (`list_elements: true`)
* Supports Cloudflare, PerimeterX, DataDome, Akamai
* Built-in rotating proxies
* Target a specific exit country (`proxy_country`)
* Minimal input (only URL required)

---

## 🖱️ NEW: Interact with the page before capturing (`steps`)

Some pages only show what you need **after** you interact — type into a search box, click a button, accept a cookie banner, or wait for results to load. With `steps` you describe those actions and ScrapeUnblocker runs them in a real browser, then returns the resulting page.

`steps` is an **ordered list** of actions. Each action is an object with an `action` and, depending on the action, a `selector` and/or a `value`:

| Action | What it does | Needs |
|--------|--------------|-------|
| `wait_for` | Wait until an element appears | `selector` |
| `wait_for_text` | Wait until some text appears on the page | `value` |
| `wait` | Wait a fixed number of milliseconds | `value` (ms) |
| `click` | Click an element | `selector` |
| `type` | Type text into an input | `selector`, `value` |
| `select` | Pick an option in a `<select>` | `selector`, `value` |
| `press_key` | Press a keyboard key (e.g. `Enter`) | `value` |
| `scroll` | Scroll the page (e.g. `bottom`) | `value` |

**Example — search for "bmw" and wait for the results:**

```json
{
  "url": "https://example.com",
  "steps": [
    { "action": "type", "selector": "#q", "value": "bmw" },
    { "action": "press_key", "value": "Enter" },
    { "action": "wait_for", "selector": ".results" }
  ]
}
```

* Steps run **once** (they are non-idempotent — a step may submit a form), so this mode does not auto-retry.
* If a step fails (bad selector, element never appeared), the Actor returns a structured error telling you **which step failed** (`step_index`, `action`, `reason`) plus the page HTML at that point — so you can fix the selector.

---

## 🔎 NEW: Discover what to click (`list_elements`)

Not sure which selector to target? Set `list_elements: true` and, instead of HTML, the Actor returns the page's **interactive elements** (buttons, inputs, selects, links, forms) with ready-to-use selectors. Use it to build your `steps` list.

```json
{
  "url": "https://example.com",
  "list_elements": true
}
```

Returns:

```json
{
  "url": "https://example.com",
  "count": 3,
  "elements": [
    { "tag": "input", "selector": "#q", "id": "q", "text": "" },
    { "tag": "button", "selector": ".search-btn", "text": "Search" }
  ]
}
```

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

Clean Markdown (main content only, unless `main_content_only` is `false`):

```json
{
  "url": "https://example.com",
  "markdown": true
}
```

Target a specific exit country (optional):

```json
{
  "url": "https://example.com",
  "proxy_country": "DE"
}
```

`proxy_country` is a two-letter ISO country code. Leave it empty (Random) to let ScrapeUnblocker pick the best country for the target. Available: AT, BE, BG, BR, CA, CH, CN, DE, DK, EE, ES, FR, GB, GR, HK, HR, IE, IL, IT, JP, KR, LT, LU, LV, MD, NL, NO, PL, RO, RS, SE, SG, TH, TR, TW, US.

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
  "data": {
    "results": {
      "items": [
        { "title": "BMW i5 2024 ...", "url": "https://autoplius.lt/skelbimai/..." }
      ]
    }
  }
}
```

**With `markdown: true`** - one dataset item with the page as Markdown:

```json
{
  "url": "https://example.com",
  "markdown": "# Page title\n\nThe main content of the page..."
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
* Feeding clean Markdown straight into LLMs, AI agents and RAG pipelines
* Monitoring competitor pages

**Page does not exist** — if the site answers HTTP 404 or 410, no dataset item is created and you are not charged. The run still succeeds; the `ERRORS` record in the key-value store explains it, and `OUTPUT` holds the site's own not-found page:

```json
[
  {
    "url": "https://example.com/removed-product",
    "error": "The page does not exist: the site answered HTTP 404. ...",
    "origin_status": 404
  }
]
```

---

## ⚠️ Important notes

* **Retries are expected:** Due to the nature of complex anti-bot systems, requests might not always succeed on the first try and you may encounter errors. If a request fails, we highly recommend trying again, as subsequent attempts are often successful.
* **Nothing to parse still returns the page:** with `parsed_data: true`, a page that loads but holds no structured data creates one dataset item with `"data_extracted": false`, a `detail` line and the rendered page in `html` - charged like any other result.
* **A missing page is final:** a 404/410 from the site is its own answer, not a block, so retrying returns the same result. It is recorded in `ERRORS` and not charged.
* When `parsed_data: true` is used on a brand-new domain, extraction rules may still be generating — the Actor automatically waits and retries until the parsed result is ready.
* Response time depends on target protection level

---

## 💡 More tools, docs & functionality

ScrapeUnblocker also offers SERP scraping, image fetching, cookies retrieval and more.

👉 Explore the full documentation and feature set at **[scrapeunblocker.com](https://www.scrapeunblocker.com/?utm_source=apify&utm_medium=integration&utm_campaign=apify-actor)**
