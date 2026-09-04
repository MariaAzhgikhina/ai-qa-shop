from playwright.sync_api import Page, expect


def test_max_quantity(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_test_id("add-to-cart-3").click()

    quantity = page.get_by_label("Qty")
    quantity.fill("11")
    page.get_by_role("button", name="Update").click()

    expect(page.get_by_role("alert")).to_have_text("Maximum quantity of one product is 10")
    expect(quantity).to_have_value("1")
