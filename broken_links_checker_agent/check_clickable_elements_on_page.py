import asyncio
from playwright.async_api import async_playwright

async def scrollToBottom(page):
    previous_height = await page.evaluate("document.body.scrollHeight")
    while True:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)  # Esperar un tiempo para que se carguen los nuevos elementos
        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

async def checkClickableElementsOnPage(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir="videos/",
            record_har_path="trace.har"
        )

        page = await context.new_page()

        await page.goto(url)

        await page.wait_for_timeout(3000)

        await scrollToBottom(page)


        clickableElements = ['.card']

        for clickableElement in clickableElements:
            print(f"Checking clickable elements of type: {clickableElement}")
            elements = await page.query_selector_all(clickableElement)
            print(f"Found {len(elements)} elements of type {clickableElement}")

            for i in enumerate(elements):
                try:
                    elements = await page.query_selector_all(clickableElement)
                    element = elements[i[0]]

                    title_element = await element.query_selector('h2')
                    title = await title_element.text_content() if title_element else "No title found"
                    print(f"Element title: {title.strip()}")

                    contains_lock_icon = await element.query_selector('mat-icon[svgicon="my-lock"]')
                    if contains_lock_icon:
                        print(f"Skipping element {i[0]} because it contains a lock icon")
                    else:
                        await element.click()
                        await page.wait_for_timeout(3000)
                        current_url = page.url
                        print(f"Clicked on element {i[0]} and navigated to {current_url}")
                        
                        await page.go_back()
                        await page.wait_for_timeout(3000)
                        await scrollToBottom(page)
                except Exception as e:
                    print(f"Error clicking on element: {e}")
                
        await browser.close()        
    
# URL de ejemplo
url = "https://soyzen.com/home"

# Ejecutar la función
asyncio.run(checkClickableElementsOnPage(url))
