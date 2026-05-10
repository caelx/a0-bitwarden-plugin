from __future__ import annotations

import json

from helpers.install_manifest import load_manifest, save_manifest
from helpers.redaction import redact_data, redact_text


def test_redacts_known_secret_env_assignments() -> None:
    text = "BW_CLIENT_SECRET=abc BW_PASSWORD=hunter2 BW_SESSION=session"
    assert "abc" not in redact_text(text)
    assert "hunter2" not in redact_text(text)
    assert "session" not in redact_text(text)


def test_redacts_secret_keys_in_nested_data() -> None:
    data = {"outer": {"BW_CLIENT_SECRET": "abc", "safe": "ok"}}
    redacted = redact_data(data)
    assert redacted["outer"]["BW_CLIENT_SECRET"] == "<redacted>"
    assert redacted["outer"]["safe"] == "ok"


def test_redaction_preserves_secret_presence_summaries() -> None:
    data = {"env": {"BW_CLIENT_SECRET": {"present": False}}}
    assert redact_data(data)["env"]["BW_CLIENT_SECRET"]["present"] is False


def test_manifest_save_redacts_secrets(tmp_path) -> None:
    path = tmp_path / "manifest.json"
    save_manifest({"warnings": [], "auth": {"BW_SESSION": "secret"}}, path=path)
    raw = path.read_text(encoding="utf-8")
    assert "secret" not in raw
    assert json.loads(raw)["auth"]["BW_SESSION"] == "<redacted>"
    loaded = load_manifest(path)
    assert loaded["auth"]["BW_SESSION"] == "<redacted>"
