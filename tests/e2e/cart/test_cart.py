from playwright.sync_api import Page, expect


def test_product_can_be_added_to_cart(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_test_id("add-to-cart-1").click()

    expect(page).to_have_url(f"{base_url}/cart")
    expect(page.get_by_test_id("cart-item")).to_contain_text("Wireless Headphones")
    expect(page.get_by_test_id("cart-total")).to_have_text("$79.90")
