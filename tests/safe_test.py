import safe


class FakeSt:
    def __init__(self):
        self.warnings = []

    def warning(self, message):
        self.warnings.append(message)


def test_render_safely_shows_notice_instead_of_raising(monkeypatch):
    fake = FakeSt()
    monkeypatch.setattr(safe, "st", fake)

    def broken():
        raise ConnectionError("blocked")

    safe.render_safely("News", broken)

    assert len(fake.warnings) == 1
    assert "News could not load right now" in fake.warnings[0]
    assert "ConnectionError" in fake.warnings[0]


def test_render_safely_passes_arguments_and_stays_quiet_on_success(monkeypatch):
    fake = FakeSt()
    monkeypatch.setattr(safe, "st", fake)
    seen = []

    safe.render_safely("Portfolio", lambda user: seen.append(user), "test1")

    assert seen == ["test1"]
    assert fake.warnings == []
