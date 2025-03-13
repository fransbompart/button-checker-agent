import asyncio
from playwright.async_api import async_playwright

async def operator_log_in_tribu_deportiva():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            record_video_dir="videos/",  
            record_har_path="trace.har" 
        )
        page = await context.new_page()
        
        await page.goto("https://tribudeportiva.com/auth/login")

        # await page.click('button[aria-label="Digitel Logo Image"]')
        await page.click('img[src="https://media.tribudeportiva.com/operators/digitel.png"]')

        await page.click('.mat-mdc-form-field-type-mat-select')

        await page.click('div[role="listbox"] >> text=0412')

        await page.fill('input[formcontrolname="phone"]', '2313877')

        # Hacer clic en el botón de registro
        await page.click('#btn-signup')

        # Esperar un tiempo para que la navegación se complete
        await page.wait_for_timeout(3000)

        # Obtener la URL actual de la página
        url = page.url
        print(f'Current URL: {url}')

        await page.click('button[aria-haspopup="menu"] mat-icon[svgicon="my-profile-circled"]')
        await page.wait_for_timeout(3000)

        expected_text = "584122313877@tribudeportivaguest.com"
        actual_text = await page.text_content('span.email')
        assert actual_text == expected_text, f"Expected text '{expected_text}', got '{actual_text}'"

        print(actual_text)

        await browser.close()

asyncio.run(operator_log_in_tribu_deportiva())
