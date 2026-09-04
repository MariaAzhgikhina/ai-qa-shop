from playwright.sync_api import Page, expect


def test_cart_total(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_test_id("add-to-cart-1").click()
    page.get_by_label("Qty").fill("2")
    page.get_by_role("button", name="Update").click()

    expect(page.get_by_test_id("cart-total")).to_have_text("$79.90")
