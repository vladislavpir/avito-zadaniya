from __future__ import annotations

import allure
import pytest

from framework.api_client import AdsApiClient
from framework.assertions import assert_error_response, assert_statistics_response
from framework.generators import ZERO_UUID


@allure.feature("Ads API")
@allure.story("Get item statistics")
class TestGetStatistics:
    @allure.title("Statistics endpoint returns created item statistics")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_statistics_returns_created_item_statistics(
        self,
        api_client: AdsApiClient,
        created_item: dict,
    ) -> None:
        response = api_client.get_statistics(created_item["id"])

        statistics = assert_statistics_response(
            response,
            expected_statistics=created_item["statistics"],
        )
        assert len(statistics) == 1

    @allure.title("Statistics endpoint with invalid UUID returns 400")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_statistics_with_invalid_uuid_returns_400(self, api_client: AdsApiClient) -> None:
        response = api_client.get_statistics("not-a-uuid")

        assert_error_response(
            response,
            expected_status_code=400,
            expected_status_value="400",
            expected_message="передан некорректный идентификатор объявления",
        )

    @allure.title("Statistics endpoint with nonexistent UUID returns 404")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_statistics_with_nonexistent_uuid_returns_404(
        self,
        api_client: AdsApiClient,
    ) -> None:
        response = api_client.get_statistics(ZERO_UUID)

        assert_error_response(
            response,
            expected_status_code=404,
            expected_status_value="404",
            expected_message=f"statistic {ZERO_UUID} not found",
        )