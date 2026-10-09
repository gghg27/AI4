import os
import subprocess
import tempfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
MKDOCS_PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"


def build_site(site_dir: Path, configured: bool | None) -> None:
    env = os.environ.copy()
    if configured is None:
        for key in ("GISCUS_REPO_ID", "GISCUS_CATEGORY", "GISCUS_CATEGORY_ID"):
            env.pop(key, None)
    else:
        env.update(
            GISCUS_REPO_ID="R_test" if configured else "",
            GISCUS_CATEGORY="General",
            GISCUS_CATEGORY_ID="DIC_test" if configured else "",
        )
    subprocess.run(
        [str(MKDOCS_PYTHON), "-m", "mkdocs", "build", "--strict", "--site-dir", str(site_dir)],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


with tempfile.TemporaryDirectory() as tmp:
    default_dir = Path(tmp) / "default"
    build_site(default_dir, configured=None)
    default_html = (default_dir / "index.html").read_text(encoding="utf-8")
    assert 'data-repo-id="R_kgDOVBFmfQ"' in default_html
    assert 'data-category-id="DIC_kwDOVBFmfc4DHVx1"' in default_html

    site_dir = Path(tmp) / "configured"
    build_site(site_dir, configured=True)
    pages = list(site_dir.rglob("index.html"))
    assert pages, "MkDocs did not generate content pages"
    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert 'class="guide-comments"' in html, page
        assert 'data-repo="gghg27/ai_discuss"' in html, page
        assert 'data-repo-id="R_test"' in html, page
        assert 'data-category-id="DIC_test"' in html, page

    handler = partial(SimpleHTTPRequestHandler, directory=str(site_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.route(
                "https://giscus.app/client.js",
                lambda route: route.fulfill(
                    status=200, content_type="text/javascript", body=""
                ),
            )
            page.goto(f"http://127.0.0.1:{server.server_port}/")
            comments = page.locator(".guide-comments__thread script")
            comments.wait_for(state="attached")
            assert comments.get_attribute("data-theme") == "light"
            assert comments.get_attribute("data-mapping") == "pathname"
            assert comments.get_attribute("data-strict") == "1"
            home_path = urlsplit(page.url).path
            page.locator('label[title="切换到深色模式"]').click(force=True)
            page.get_by_role("link", name="计算机基础扫盲").first.click()
            page.wait_for_url("**/01-computer/*/")
            comments = page.locator(".guide-comments__thread script")
            comments.wait_for(state="attached")
            assert comments.get_attribute("data-theme") == "dark"
            assert comments.get_attribute("data-mapping") == "pathname"
            assert comments.get_attribute("data-strict") == "1"
            assert urlsplit(page.url).path != home_path
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()

    unconfigured_dir = Path(tmp) / "unconfigured"
    build_site(unconfigured_dir, configured=False)
    assert 'class="guide-comments"' not in (
        unconfigured_dir / "index.html"
    ).read_text(encoding="utf-8")

print("Comments template verification passed for every content page.")
