from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:8000/"
ARTIFACTS = Path("artifacts")


def assert_no_horizontal_overflow(page, viewport_width: int) -> None:
    metrics = page.locator("body").evaluate(
        "el => ({scrollWidth: el.scrollWidth, clientWidth: el.clientWidth})"
    )
    assert metrics["scrollWidth"] <= max(metrics["clientWidth"], viewport_width), metrics


def verify_desktop(browser) -> None:
    errors: list[str] = []
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.emulate_media(color_scheme="light")
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(f"PAGEERROR: {error}"))
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.locator(".route-card").first.wait_for(state="visible")
    page.wait_for_function("document.body.hasAttribute('data-md-color-scheme')")

    assert page.title().startswith("AI 不完全指北")
    assert page.locator("h1").first.inner_text().startswith("AI 不完全指北")
    assert page.locator(".md-tabs").count() == 0

    primary_sidebar = page.locator(".md-sidebar--primary")
    assert primary_sidebar.is_visible()
    assert primary_sidebar.get_by_role("link", name="首页", exact=True).is_visible()
    assert primary_sidebar.get_by_role("link", name="引言", exact=True).is_visible()
    assert primary_sidebar.locator(
        "label.md-nav__link", has_text="第一部分：计算机第一课"
    ).is_visible()
    assert primary_sidebar.locator(
        "label.md-nav__link", has_text="第二部分：大模型与 Agent"
    ).is_visible()
    assert primary_sidebar.locator(
        "label.md-nav__link", has_text="第三部分：链接合集"
    ).is_visible()
    assert primary_sidebar.get_by_text("计算机基础扫盲", exact=True).is_visible()
    assert primary_sidebar.get_by_text("底层原理", exact=True).is_visible()
    assert primary_sidebar.get_by_text("魔法", exact=True).is_visible()
    assert primary_sidebar.get_by_role("link", name="关于", exact=True).is_visible()

    primary_box = primary_sidebar.bounding_box()
    content_box = page.locator(".md-content").bounding_box()
    secondary_box = page.locator(".md-sidebar--secondary").bounding_box()
    assert primary_box is not None
    assert content_box is not None
    assert secondary_box is not None
    assert primary_box["x"] < content_box["x"] < secondary_box["x"]
    assert content_box["width"] >= 640

    assert page.locator(".route-card").count() == 3
    assert page.locator(".route-grid").evaluate(
        "el => getComputedStyle(el).gridTemplateColumns.split(' ').length"
    ) == 3
    route_card = page.locator(".route-card").first
    assert route_card.evaluate(
        """el => (
            parseFloat(getComputedStyle(el).minHeight) /
            parseFloat(getComputedStyle(document.documentElement).fontSize)
        )"""
    ) <= 9.5
    assert page.locator(".md-header").evaluate(
        "el => getComputedStyle(el).backgroundColor"
    ) == "rgb(228, 242, 255)"
    assert page.locator(".md-footer-meta__inner").evaluate(
        "el => getComputedStyle(el).color"
    ) == "rgb(82, 98, 122)"
    assert_no_horizontal_overflow(page, 1440)

    ARTIFACTS.mkdir(exist_ok=True)
    page.screenshot(path=str(ARTIFACTS / "home-desktop.png"), full_page=True)

    page.locator('label[title="切换到深色模式"]').click(force=True)
    page.wait_for_function(
        "document.body.getAttribute('data-md-color-scheme') === 'slate'"
    )
    page.screenshot(path=str(ARTIFACTS / "home-dark.png"), full_page=True)

    page.goto(f"{BASE_URL}02-ai-and-agents/", wait_until="domcontentloaded")
    assert page.locator("h1").first.inner_text().startswith("第二部分")

    page.goto(
        f"{BASE_URL}02-ai-and-agents/底层原理/",
        wait_until="domcontentloaded",
    )
    assert page.locator("h1").first.inner_text().startswith("底层原理")

    page.goto(
        f"{BASE_URL}01-computer/Markdown语法详细教程/",
        wait_until="domcontentloaded",
    )
    assert page.locator("h1").first.inner_text().startswith("Markdown 语法详细教程")
    mermaid_example = page.locator("p code", has_text="flowchart TD").first
    mermaid_example.wait_for(state="visible")
    assert "```mermaid" in mermaid_example.inner_text()
    assert errors == [], errors
    page.close()


def verify_mobile(browser) -> None:
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.emulate_media(color_scheme="light")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.locator(".route-card").first.wait_for(state="visible")

    assert page.locator(".route-grid").evaluate(
        "el => getComputedStyle(el).gridTemplateColumns.split(' ').length"
    ) == 1
    assert page.locator(".route-card").count() == 3
    assert_no_horizontal_overflow(page, 390)

    primary_box = page.locator(".md-sidebar--primary").bounding_box()
    assert primary_box is not None
    assert primary_box["x"] < 0
    assert primary_box["x"] + primary_box["width"] <= 0
    assert not page.locator(".md-sidebar--secondary").is_visible()

    page.locator('label[for="__drawer"].md-header__button').click()
    assert page.locator("#__drawer").is_checked()
    assert page.get_by_role("link", name="引言").first.is_visible()
    page.locator('label[for="__drawer"].md-overlay').click()
    assert not page.locator("#__drawer").is_checked()
    page.wait_for_function(
        """() => {
            const rect = document.querySelector('.md-sidebar--primary')
                .getBoundingClientRect()
            return rect.right <= 0
        }"""
    )

    ARTIFACTS.mkdir(exist_ok=True)
    page.screenshot(path=str(ARTIFACTS / "home-mobile.png"), full_page=True)
    page.close()


def verify_tablet(browser) -> None:
    page = browser.new_page(viewport={"width": 1024, "height": 900})
    page.emulate_media(color_scheme="light")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.locator(".route-card").first.wait_for(state="visible")

    primary_box = page.locator(".md-sidebar--primary").bounding_box()
    assert primary_box is not None
    assert primary_box["x"] >= 0
    assert not page.locator(".md-sidebar--secondary").is_visible()
    assert not page.locator('label[for="__drawer"].md-header__button').is_visible()
    assert_no_horizontal_overflow(page, 1024)
    page.close()


with sync_playwright() as playwright:
    chromium = playwright.chromium.launch(headless=True)
    verify_desktop(chromium)
    verify_tablet(chromium)
    verify_mobile(chromium)
    chromium.close()

print("Site verification passed: desktop, dark mode, tablet, and mobile.")
