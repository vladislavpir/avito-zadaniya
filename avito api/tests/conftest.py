from __future__ import annotations

from collections.abc import Callable

import pytest

from framework.api_client import AdsApiClient
from framework.assertions import assert_create_item_response, assert_item_list_response
from framework.factories import build_item_payload
from framework.generators import SELLER_ID_MAX, SELLER_ID_MIN, generate_seller_id


@pytest.fixture(scope="session")
def api_client() -> AdsApiClient:
    return AdsApiClient()


@pytest.fixture
def item_payload_factory() -> Callable[..., dict]:
    return build_item_payload


@pytest.fixture
def created_item(api_client: AdsApiClient, item_payload_factory: Callable[..., dict]) -> dict:
    payload = item_payload_factory()
    response = api_client.create_item(payload)
    payload["id"] = assert_create_item_response(response)
    return payload


@pytest.fixture(params=[SELLER_ID_MIN, SELLER_ID_MAX], ids=["seller-min", "seller-max"])
def boundary_seller_id(request: pytest.FixtureRequest) -> int:
    return int(request.param)


@pytest.fixture
def empty_seller_id(api_client: AdsApiClient) -> int:
    for _ in range(20):
        seller_id = generate_seller_id()
        response = api_client.get_seller_items(seller_id)
        if response.status_code == 200 and assert_item_list_response(response) == []:
            return seller_id
    pytest.skip("Could not find an empty sellerId in 20 attempts on the shared environment")