from __future__ import annotations

import allure
import pytest

from framework.api_client import AdsApiClient
from framework.assertions import (
    assert_create_item_response,
    assert_item_list_response,
    assert_statistics_response,
)
from framework.factories import build_item_payload


@allure.feature("Ads API")
@allure.story("End-to-end flows")
class TestE2EItemFlows:
    @allure.title("Create item then read item and statistics")
    @pytest.mark.e2e
    @pytest.mark.regression
    def test_e2e_create_then_get_item_then_get_statistics(self, api_client: AdsApiClient) -> None:
        payload = build_item_payload()

        create_response = api_client.create_item(payload)
        payload["id"] = assert_create_item_response(create_response)

        item_response = api_client.get_item(payload["id"])
        assert_item_list_response(item_response, expected_count=1, expected_item=payload)

        statistics_response = api_client.get_statistics(payload["id"])
        assert_statistics_response(statistics_response, expected_statistics=payload["statistics"])

    @allure.title("Create two items then read both by seller")
    @pytest.mark.e2e
    @pytest.mark.regression
    def test_e2e_create_two_items_then_get_them_by_seller(self, api_client: AdsApiClient) -> None:
        first_payload = build_item_payload()
        second_payload = build_item_payload(seller_id=first_payload["sellerId"])

        first_payload["id"] = assert_create_item_response(api_client.create_item(first_payload))
        second_payload["id"] = assert_create_item_response(api_client.create_item(second_payload))

        seller_response = api_client.get_seller_items(first_payload["sellerId"])
        items = assert_item_list_response(seller_response)
        indexed = {str(item.id): item for item in items}

        assert first_payload["id"] in indexed
        assert second_payload["id"] in indexed
        assert indexed[first_payload["id"]].statistics.model_dump() == first_payload["statistics"]
        assert indexed[second_payload["id"]].statistics.model_dump() == second_payload["statistics"]
