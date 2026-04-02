from __future__ import annotations

from framework.generators import generate_name, generate_seller_id


def build_item_payload(
    *,
    seller_id: int | None = None,
    name: str | None = None,
    price: int = 1000,
    likes: int = 1,
    view_count: int = 10,
    contacts: int = 2,
) -> dict:
    return {
        "sellerId": seller_id if seller_id is not None else generate_seller_id(),
        "name": name if name is not None else generate_name(),
        "price": price,
        "statistics": {
            "likes": likes,
            "viewCount": view_count,
            "contacts": contacts,
        },
    }
