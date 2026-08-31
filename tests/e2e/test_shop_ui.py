from playwright.sync_api import Page, expect


def test_catalog_opens(page: Page, base_url: str):
    page.goto(base_url)

    expect(page).to_have_title("Catalog · AI QA Shop")
    expect(page.get_by_test_id("product-card")).to_have_count(9)


def test_product_can_be_added_to_cart(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_test_id("add-to-cart-1").click()

    expect(page).to_have_url(f"{base_url}/cart")
    expect(page.get_by_test_id("cart-item")).to_contain_text("Wireless Headphones")
    expect(page.get_by_test_id("cart-total")).to_have_text("$79.90")


def test_checkout_happy_path(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_test_id("add-to-cart-2").click()
    page.get_by_test_id("checkout-link").click()
    page.get_by_test_id("customer-name").fill("Taylor Green")
    page.get_by_test_id("email").fill("taylor@example.com")
    page.get_by_test_id("delivery-address").fill("25 River Road")
    page.get_by_test_id("place-order").click()

    expect(page.get_by_test_id("order-confirmation")).to_be_visible()
    expect(page.get_by_test_id("order-id")).to_contain_text("#")
    expect(page.get_by_test_id("cart-link")).to_contain_text("0")
