from __future__ import annotations

import allure
import pytest

from framework.api_client import AdsApiClient
from framework.assertions import (
    assert_create_item_response,
    assert_error_response,
    assert_item_list_response,
    assert_seller_items_all_belong_to_seller,
)
from framework.factories import build_item_payload


@allure.feature("Ads API")
@allure.story("Get seller items")
class TestGetSellerItems:
    @allure.title("Seller items response contains created item")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_seller_items_contains_created_item(
        self,
        api_client: AdsApiClient,
        created_item: dict,
    ) -> None:
        response = api_client.get_seller_items(created_item["sellerId"])

        items = assert_item_list_response(response, expected_item=created_item)
        assert_seller_items_all_belong_to_seller(items, created_item["sellerId"])

    @allure.title("Seller items response contains two created items for one seller")
    @pytest.mark.regression
    def test_get_seller_items_contains_two_created_items_for_same_seller(
        self,
        api_client: AdsApiClient,
    ) -> None:
        first_payload = build_item_payload()
        second_payload = build_item_payload(seller_id=first_payload["sellerId"])

        first_payload["id"] = assert_create_item_response(api_client.create_item(first_payload))
        second_payload["id"] = assert_create_item_response(api_client.create_item(second_payload))

        seller_response = api_client.get_seller_items(first_payload["sellerId"])

        items = assert_item_list_response(seller_response)
        returned_ids = {str(item.id) for item in items}
        assert {first_payload["id"], second_payload["id"]}.issubset(returned_ids)
        assert_seller_items_all_belong_to_seller(items, first_payload["sellerId"])

    @allure.title("Fresh sellerId returns empty item list")
    @pytest.mark.negative
    @pytest.mark.edge
    @pytest.mark.regression
    def test_get_seller_items_for_empty_seller_returns_empty_list(
        self,
        api_client: AdsApiClient,
        empty_seller_id: int,
    ) -> None:
        response = api_client.get_seller_items(empty_seller_id)

        assert assert_item_list_response(response) == []

    @allure.title("Invalid sellerId returns 400")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_seller_items_with_invalid_seller_id_returns_400(
        self,
        api_client: AdsApiClient,
    ) -> None:
        response = api_client.get_seller_items("abc")

        assert_error_response(
            response,
            expected_status_code=400,
            expected_status_value="400",
            expected_message="передан некорректный идентификатор продавца",
        )