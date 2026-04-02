from __future__ import annotations

import random
import time
import uuid

SELLER_ID_MIN = 111111
SELLER_ID_MAX = 999999
ZERO_UUID = "00000000-0000-0000-0000-000000000000"


def generate_seller_id() -> int:
    return random.randint(SELLER_ID_MIN, SELLER_ID_MAX)


def generate_name(prefix: str = "qa-item") -> str:
    return f"{prefix}-{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"