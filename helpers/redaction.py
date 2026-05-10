from __future__ import annotations

import re
from typing import Any

SECRET_KEYS = {
    "bw_client_id",
    "bw_client_secret",
    "bw_password",
    "bw_session",
    "client_id",
    "client_secret",
    "password",
    "session",
    "token",
    "access_token",
    "refresh_token",
    "secret",
}

SECRET_PATTERNS = [
    re.compile(r"(?i)(BW_CLIENT_ID|BW_CLIENT_SECRET|BW_PASSWORD|BW_SESSION)=([^\s]+)"),
    re.compile(r"(?i)(client_secret|password|session|token)[\"']?\s*[:=]\s*[\"']?([^\"'\s,}]+)"),
]


def redact_text(value: str) -> str:
    text = value
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(lambda match: f"{match.group(1)}=<redacted>", text)
    return text


def redact_data(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[Any, Any] = {}
        for key, item in value.items():
            if _is_secret_key(str(key)):
                if isinstance(item, (dict, list)):
                    redacted[key] = redact_data(item)
                elif isinstance(item, str):
                    redacted[key] = "<redacted>" if item else item
                else:
                    redacted[key] = item
            else:
                redacted[key] = redact_data(item)
        return redacted
    if isinstance(value, list):
        return [redact_data(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def trim_output(value: str | None, limit: int = 4000) -> str:
    return redact_text((value or "")[-limit:])


def _is_secret_key(key: str) -> bool:
    normalized = key.strip().lower()
    return normalized in SECRET_KEYS or any(
        part in normalized for part in ("secret", "password", "token")
    )
