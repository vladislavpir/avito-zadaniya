from __future__ import annotations

import allure
import pytest

from framework.api_client import AdsApiClient
from framework.assertions import assert_error_response, assert_item_list_response
from framework.generators import ZERO_UUID


@allure.feature("Ads API")
@allure.story("Get item by ID")
class TestGetItem:
    @allure.title("Get item by ID returns created item")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_item_by_id_returns_created_item(
        self,
        api_client: AdsApiClient,
        created_item: dict,
    ) -> None:
        response = api_client.get_item(created_item["id"])

        items = assert_item_list_response(response, expected_count=1, expected_item=created_item)
        assert items[0].createdAt

    @allure.title("Get item with invalid UUID returns 400")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_item_with_invalid_uuid_returns_400(self, api_client: AdsApiClient) -> None:
        response = api_client.get_item("not-a-uuid")

        assert_error_response(
            response,
            expected_status_code=400,
            expected_status_value="400",
            expected_message="ID айтема не UUID: not-a-uuid",
        )

    @allure.title("Get item with nonexistent UUID returns 404")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_item_with_nonexistent_uuid_returns_404(self, api_client: AdsApiClient) -> None:
        response = api_client.get_item(ZERO_UUID)

        assert_error_response(
            response,
            expected_status_code=404,
            expected_status_value="404",
            expected_message=f"item {ZERO_UUID} not found",
        )
