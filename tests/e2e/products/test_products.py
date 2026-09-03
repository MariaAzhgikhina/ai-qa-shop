from playwright.sync_api import Page, expect


def test_catalog_opens(page: Page, base_url: str):
    page.goto(base_url)

    expect(page).to_have_title("Catalog · AI QA Shop")
    expect(page.get_by_test_id("product-card")).to_have_count(9)
