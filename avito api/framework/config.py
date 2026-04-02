from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://qa-internship.avito.com")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "15"))


settings = Settings()
