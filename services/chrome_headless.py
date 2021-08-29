from typing import List

from pyppeteer.launcher import Launcher


class ChromeHeadlessService:
    def __init__(self):
        self.launcher = Launcher(
            {
                "headless": True,
                'executablePath': '/usr/bin/google-chrome',
            },
            args=[
                '--no-sandbox',
                # '--disable-web-security',
                # '--user-data-dir=user-data',
                # "--disable-blink-features=AutomationControlled",
                # "--disable-dev-shm-usage"
                "--disable-gpu"
                # "--window-size=1680,1050",
            ],
            # defaultViewport={"width": 1920, "height": 1080}
            defaultViewport=None,
        )

    async def execute(self, method_resources: List) -> List:
        results = []
        browser = await self.launcher.launch()
        page = await browser.newPage()
        client = await page.target.createCDPSession()
        for method_resource in method_resources:
            result = await client.send(**method_resource.dict())
            results.append(result)
        await browser.close()
        return results
