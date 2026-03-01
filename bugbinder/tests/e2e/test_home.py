def test_home_title_contains_bug_text(page, live_server):
    page.goto(live_server.url)
    assert "Bug Binder" in page.title()
    # print(page.title())