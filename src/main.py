import os
import requests
import asyncio
from apify import Actor

async def main():
    async with Actor:
        print("✅ ScrapeUnblocker started")

        input_data = await Actor.get_input()
        url = input_data.get("url") if input_data else None

        if not url:
            raise Exception("Missing 'url' input")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "X-ScrapeUnblocker-Key": os.environ["SCRAPEUNBLOCKER_KEY"],
        }

        params = {"url": url}

        max_retries = 1
        attempt = 0
        response = None

        while attempt <= max_retries:
            response = requests.post(
                "https://api.scrapeunblocker.com/getPageSource",
                headers=headers,
                params=params,
            )
            
            if response.status_code == 200:
                break
            
            print(f"⚠️ Warning: Received status code {response.status_code}. Response: {response.text}")
            attempt += 1
            if attempt <= max_retries:
                print("⏳ Retrying immediately...")

        if response.status_code != 200:
            raise Exception(f"❌ ScrapeUnblocker failed after {max_retries + 1} attempts. Final status code: {response.status_code}. Response: {response.text}")

        response.encoding = "utf-8"
        html = response.text

        # 1. Save files to Key-Value Store
        await Actor.set_value("OUTPUT", html, content_type="text/html")
        await Actor.set_value("output.html", html, content_type="text/html")

        # 2. Wait until the output URL is actually accessible by the outside world
        # This forces the Actor to stay alive until the CDN/S3 has propagated the file.
        store_id = os.environ.get("APIFY_DEFAULT_KEY_VALUE_STORE_ID")
        if store_id:
            public_url = f"https://api.apify.com/v2/key-value-stores/{store_id}/records/output.html"
            print(f"⏳ Verifying public accessibility of: {public_url}")

            for i in range(30):  # Try for up to 30 seconds
                try:
                    check_resp = requests.get(public_url)
                    if check_resp.status_code == 200:
                        print(f"✅ Output is now publicly accessible (took {i}s)")
                        break
                except Exception:
                    pass
                await asyncio.sleep(1)
        else:
            await asyncio.sleep(2)

        # 3. Push data to the Dataset and finish
        await Actor.push_data({
            "url": url,
            "html": html,
        })

        if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
