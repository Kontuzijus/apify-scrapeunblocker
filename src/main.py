import os
import json
import requests
import urllib3
import asyncio
from apify import Actor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# When parsed_data is requested, the API may answer 202 with a "processing"
# payload while it generates the AI extraction rules for a new domain. Poll a
# few times before giving up instead of treating it as a hard failure.
PARSED_POLL_DELAY_S = 5
PARSED_MAX_POLLS = 6

async def main():
    async with Actor:
        print("✅ ScrapeUnblocker started")

        input_data = await Actor.get_input() or {}
        url = input_data.get("url")
        parsed_data = bool(input_data.get("parsed_data", False))
        list_elements = bool(input_data.get("list_elements", False))
        steps = input_data.get("steps") or None
        proxy_country = (input_data.get("proxy_country") or "").strip()

        if not url:
            raise Exception("Missing 'url' input")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "X-ScrapeUnblocker-Key": os.environ["SCRAPEUNBLOCKER_KEY"],
        }

        params = {"url": url}
        if parsed_data:
            params["parsed_data"] = "true"
        if list_elements:
            params["list_elements"] = "true"
        if steps:
            # Ordered browser actions, JSON-encoded into the query param.
            params["steps"] = json.dumps(steps)
        if proxy_country:
            # Two-letter ISO country code for the exit proxy (e.g. "US", "DE").
            params["proxy_country"] = proxy_country

        # parsed_data mode may need extra polls for the 202 "processing" state;
        # plain HTML mode keeps the original single-immediate-retry behaviour.
        # Steps are non-idempotent (a step may submit a form), so they run once.
        max_attempts = PARSED_MAX_POLLS if parsed_data else 2
        if steps:
            max_attempts = 1
        response = None

        for attempt in range(max_attempts):
            response = requests.post(
                "https://api.scrapeunblocker.com/getPageSource",
                headers=headers,
                params=params,
                verify=False,
            )

            if response.status_code == 200:
                break

            # AI extraction rules still being generated — wait and re-poll.
            if parsed_data and response.status_code == 202:
                print(f"⏳ Parsing in progress (202). Waiting {PARSED_POLL_DELAY_S}s and re-polling... ({attempt + 1}/{max_attempts})")
                await asyncio.sleep(PARSED_POLL_DELAY_S)
                continue

            print(f"⚠️ Warning: Received status code {response.status_code}. Response: {response.text[:500]}")
            if attempt < max_attempts - 1:
                print("⏳ Retrying immediately...")

        # A user step failed at run time (bad selector, element never appeared).
        # This is a definitive answer, not a transient failure - surface the
        # structured error plus the page state instead of a bare exception.
        if steps and response is not None and response.status_code == 422:
            try:
                err = response.json()
            except Exception:
                err = {"error": "step_failed", "detail": response.text[:500]}
            print(f"⚠️ Step {err.get('step_index')} ({err.get('action')}) failed: {err.get('reason')}")
            await Actor.set_value("OUTPUT", json.dumps(err, ensure_ascii=False), content_type="application/json")
            await Actor.push_data({"url": url, "step_error": err})
            return

        if response is None or response.status_code != 200:
            status = response.status_code if response is not None else "no response"
            body = response.text[:500] if response is not None else ""
            raise Exception(f"❌ ScrapeUnblocker failed after {max_attempts} attempts. Final status code: {status}. Response: {body}")

        if list_elements:
            # API returns { "url", "count", "elements": [...] }.
            payload = response.json()
            await Actor.set_value("OUTPUT", json.dumps(payload, ensure_ascii=False), content_type="application/json")
            await Actor.push_data(payload)
        elif parsed_data:
            # API returns { "data": <parsed JSON, shape varies by page type> }.
            payload = response.json()
            data = payload.get("data", payload)

            await Actor.set_value("OUTPUT", json.dumps(data, ensure_ascii=False), content_type="application/json")

            # Push the parsed JSON as a single dataset item under a stable "data"
            # key (matches the README contract and lets the dataset schema render
            # it as an Object field). Nesting also avoids spreading a non-dict
            # (the parsed payload can be a list).
            await Actor.push_data({"url": url, "data": data})
        else:
            response.encoding = "utf-8"
            html = response.text

            # Save to Key-Value Store (OUTPUT is what run-sync returns)
            await Actor.set_value("OUTPUT", html, content_type="text/html")

            # Push data to the Dataset
            await Actor.push_data({
                "url": url,
                "html": html,
            })

if __name__ == "__main__":
    asyncio.run(main())
