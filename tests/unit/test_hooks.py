from __future__ import annotations

import hooks


def test_install_hook_is_lightweight(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(hooks, "__file__", str(tmp_path / "hooks.py"))
    assert hooks.install() is True
    assert (tmp_path / ".bitwarden").is_dir()
