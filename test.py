from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context(**playwright.devices["Desktop Firefox"])
    # Open new page
    page = context.new_page()
    # Go to https://noonoo21.tv/drama
    page.goto("https://noonoo21.tv/drama")
    # Click .lazy >> nth=0
    # with page.expect_navigation(url="https://noonoo21.tv/drama/25208"):
    with page.expect_navigation():
        page.locator(".lazy").first.click()
    # expect(page).to_have_url("https://noonoo21.tv/drama/25208#ac47d7184GdhXdG5")
    # Go to https://noonoo21.tv/drama/25208#ac47d7184GdhXdG5
    page.goto("https://noonoo21.tv/drama/25208#ac47d7184GdhXdG5")
    # Click path >> nth=0
    # #player > div > div.container > div.player-poster.clickable > div > svg > path
    page.frame_locator("iframe").first.locator("path").first.click()

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
