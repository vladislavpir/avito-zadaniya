from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

from requests import Response

from framework.models import (
    CreateItemResponseModel,
    ErrorResponseModel,
    ItemModel,
    StatisticsModel,
    StatisticsResponseEntryModel,
)

UUID_PATTERN = re.compile(
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    re.IGNORECASE,
)


def parse_json_response(response: Response) -> Any:
    try:
        return response.json()
    except ValueError as exc:
        raise AssertionError(f"Response is not valid JSON: {response.text}") from exc


def assert_create_item_response(response: Response) -> str:
    assert response.status_code == 200, response.text
    data = parse_json_response(response)
    payload = CreateItemResponseModel.model_validate(data)
    match = UUID_PATTERN.search(payload.status)
    assert match, f"Could not extract UUID from create response: {data}"
    return match.group(1)


def assert_error_response(
    response: Response,
    *,
    expected_status_code: int,
    expected_status_value: str,
    expected_message: str | None = None,
) -> ErrorResponseModel:
    assert response.status_code == expected_status_code, response.text
    data = parse_json_response(response)
    payload = ErrorResponseModel.model_validate(data)
    assert payload.status == expected_status_value
    assert isinstance(payload.result.message, str)
    assert payload.result.messages is None or isinstance(payload.result.messages, dict)
    if expected_message is not None:
        assert payload.result.message == expected_message
    return payload


def assert_item_response(
    item_data: dict[str, Any],
    expected_item: dict[str, Any] | None = None,
) -> ItemModel:
    item = ItemModel.model_validate(item_data)
    assert isinstance(item.name, str)
    assert isinstance(item.price, int)
    assert isinstance(item.sellerId, int)
    if expected_item is not None:
        assert str(item.id) == expected_item["id"]
        assert item.sellerId == expected_item["sellerId"]
        assert item.name == expected_item["name"]
        assert item.price == expected_item["price"]
        assert item.statistics.model_dump() == expected_item["statistics"]
    return item


def assert_item_list_response(
    response: Response,
    *,
    expected_count: int | None = None,
    expected_item: dict[str, Any] | None = None,
) -> list[ItemModel]:
    assert response.status_code == 200, response.text
    data = parse_json_response(response)
    assert isinstance(data, list), f"Expected list response, got: {type(data).__name__}"
    items = [assert_item_response(item_data) for item_data in data]
    if expected_count is not None:
        assert len(items) == expected_count
    if expected_item is not None:
        matched = [item for item in items if str(item.id) == expected_item["id"]]
        assert len(matched) == 1, f"Expected item {expected_item['id']} in response"
        assert_item_response(matched[0].model_dump(mode="json"), expected_item=expected_item)
    return items


def assert_statistics_response(
    response: Response,
    *,
    expected_statistics: dict[str, int] | None = None,
) -> list[StatisticsResponseEntryModel]:
    assert response.status_code == 200, response.text
    data = parse_json_response(response)
    assert isinstance(data, list), f"Expected list response, got: {type(data).__name__}"
    statistics = [StatisticsResponseEntryModel.model_validate(item) for item in data]
    if expected_statistics is not None:
        assert len(statistics) == 1
        assert statistics[0].model_dump() == expected_statistics
    return statistics


def assert_seller_items_all_belong_to_seller(items: Iterable[ItemModel], seller_id: int) -> None:
    for item in items:
        assert item.sellerId == seller_id


def assert_statistics_payload(statistics_data: dict[str, Any]) -> StatisticsModel:
    return StatisticsModel.model_validate(statistics_data)