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

        # parsed_data mode may need extra polls for the 202 "processing" state;
        # plain HTML mode keeps the original single-immediate-retry behaviour.
        max_attempts = PARSED_MAX_POLLS if parsed_data else 2
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

        if response is None or response.status_code != 200:
            status = response.status_code if response is not None else "no response"
            body = response.text[:500] if response is not None else ""
            raise Exception(f"❌ ScrapeUnblocker failed after {max_attempts} attempts. Final status code: {status}. Response: {body}")

        if parsed_data:
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
