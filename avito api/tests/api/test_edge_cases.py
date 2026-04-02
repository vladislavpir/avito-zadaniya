from __future__ import annotations

import allure
import pytest

from framework.api_client import AdsApiClient
from framework.assertions import (
    assert_create_item_response,
    assert_error_response,
    assert_item_list_response,
)
from framework.factories import build_item_payload


@allure.feature("Ads API")
@allure.story("Edge cases")
class TestEdgeCases:
    @allure.title("Zero values are rejected for required numeric fields")
    @pytest.mark.edge
    @pytest.mark.regression
    @pytest.mark.parametrize(
        ("payload", "expected_message"),
        [
            (build_item_payload(price=0), "поле price обязательно"),
            (build_item_payload(likes=0, view_count=1, contacts=1), "поле likes обязательно"),
        ],
        ids=["zero-price", "zero-likes"],
    )
    def test_zero_values_return_validation_error(
        self,
        api_client: AdsApiClient,
        payload: dict,
        expected_message: str,
    ) -> None:
        response = api_client.create_item(payload)

        assert_error_response(
            response,
            expected_status_code=400,
            expected_status_value="400",
            expected_message=expected_message,
        )

    @allure.title("Negative numeric values are accepted by current API")
    @pytest.mark.edge
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "payload",
        [
            build_item_payload(price=-1),
            build_item_payload(likes=-1, view_count=-2, contacts=-3),
        ],
        ids=["negative-price", "negative-statistics"],
    )
    def test_negative_numeric_values_are_persisted(
        self,
        api_client: AdsApiClient,
        payload: dict,
    ) -> None:
        create_response = api_client.create_item(payload)
        payload["id"] = assert_create_item_response(create_response)

        get_response = api_client.get_item(payload["id"])
        assert_item_list_response(get_response, expected_count=1, expected_item=payload)

    @allure.title("Long and special names are persisted")
    @pytest.mark.edge
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "name",
        [
            "x" * 300,
            "!@#$%^&*()_+[]{};:,.<>?/\\|",
            "тестовое объявление 日本語",
        ],
        ids=["very-long-name", "special-chars", "non-ascii"],
    )
    def test_name_edge_cases_are_persisted(self, api_client: AdsApiClient, name: str) -> None:
        payload = build_item_payload(name=name)

        create_response = api_client.create_item(payload)
        payload["id"] = assert_create_item_response(create_response)

        get_response = api_client.get_item(payload["id"])
        assert_item_list_response(get_response, expected_count=1, expected_item=payload)