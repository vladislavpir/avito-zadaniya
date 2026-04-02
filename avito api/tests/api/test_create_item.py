from __future__ import annotations

import allure
import pytest

from framework.api_client import AdsApiClient
from framework.assertions import assert_create_item_response, assert_error_response
from framework.factories import build_item_payload


@allure.feature("Ads API")
@allure.story("Create item")
class TestCreateItem:
    @allure.title("Create item with valid payload")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_item_with_valid_payload_returns_item_id(self, api_client: AdsApiClient) -> None:
        payload = build_item_payload()

        response = api_client.create_item(payload)

        item_id = assert_create_item_response(response)
        assert item_id

    @allure.title("Create item with boundary sellerId")
    @pytest.mark.edge
    @pytest.mark.regression
    def test_create_item_with_boundary_seller_id_is_successful(
        self,
        api_client: AdsApiClient,
        boundary_seller_id: int,
    ) -> None:
        payload = build_item_payload(seller_id=boundary_seller_id)

        response = api_client.create_item(payload)

        assert_create_item_response(response)

    @allure.title("Create same payload twice returns different item IDs")
    @pytest.mark.regression
    def test_create_same_business_payload_twice_returns_two_unique_ids(
        self,
        api_client: AdsApiClient,
    ) -> None:
        payload = build_item_payload()

        first_response = api_client.create_item(payload)
        second_response = api_client.create_item(payload)

        first_id = assert_create_item_response(first_response)
        second_id = assert_create_item_response(second_response)
        assert first_id != second_id

    @allure.title("Create item without required fields returns validation error")
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.parametrize(
        ("field_name", "payload_mutator", "expected_message"),
        [
            ("name", lambda payload: payload.pop("name"), "поле name обязательно"),
            ("price", lambda payload: payload.pop("price"), "поле price обязательно"),
            ("sellerId", lambda payload: payload.pop("sellerId"), "поле sellerID обязательно"),
            ("statistics", lambda payload: payload.pop("statistics"), "поле likes обязательно"),
            (
                "statistics.likes",
                lambda payload: payload["statistics"].pop("likes"),
                "поле likes обязательно",
            ),
            (
                "statistics.viewCount",
                lambda payload: payload["statistics"].pop("viewCount"),
                "поле viewCount обязательно",
            ),
            (
                "statistics.contacts",
                lambda payload: payload["statistics"].pop("contacts"),
                "поле contacts обязательно",
            ),
        ],
        ids=[
            "missing-name",
            "missing-price",
            "missing-seller-id",
            "missing-statistics",
            "missing-likes",
            "missing-viewCount",
            "missing-contacts",
        ],
    )
    def test_create_item_with_missing_required_field_returns_400(
        self,
        api_client: AdsApiClient,
        field_name: str,
        payload_mutator,
        expected_message: str,
    ) -> None:
        payload = build_item_payload()
        payload_mutator(payload)

        response = api_client.create_item(payload)

        assert_error_response(
            response,
            expected_status_code=400,
            expected_status_value="400",
            expected_message=expected_message,
        )

    @allure.title("Create item with malformed JSON returns body parse error")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_item_with_malformed_json_returns_400(self, api_client: AdsApiClient) -> None:
        response = api_client.create_item_with_raw_body('{"sellerId": 123')

        assert_error_response(
            response,
            expected_status_code=400,
            expected_status_value="не передан объект - объявление",
            expected_message="",
        )

    @allure.title("Create item with invalid field types exposes known API defect")
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.xfail(
        reason="Known API defect: invalid typed JSON body is reported as missing body; see BUGS.md",
        strict=False,
    )
    @pytest.mark.parametrize(
        "payload",
        [
            {
                "sellerId": "abc",
                "name": "x",
                "price": 1,
                "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
            },
            {
                "sellerId": 111111,
                "name": "x",
                "price": "1",
                "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
            },
        ],
        ids=["sellerId-string", "price-string"],
    )
    def test_create_item_with_invalid_types_should_return_field_validation_error(
        self,
        api_client: AdsApiClient,
        payload: dict,
    ) -> None:
        response = api_client.create_item(payload)

        assert_error_response(
            response,
            expected_status_code=400,
            expected_status_value="400",
        )