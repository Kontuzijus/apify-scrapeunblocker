import os
import requests
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

        response = requests.post(
            "https://api.scrapeunblocker.com/getPageSource",
            headers=headers,
            params=params,
        )
        response.encoding = "utf-8"
        html = response.text

        await Actor.set_value("output.html", html, content_type="text/html")
        await Actor.push_data({
            "url": url,
            "html": html,
        })

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())