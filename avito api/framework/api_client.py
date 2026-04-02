from __future__ import annotations

import json
from typing import Any

import allure
import requests
from requests import Response

from framework.config import settings


class AdsApiClient:
    CREATE_ITEM_PATH = "/api/1/item"
    GET_ITEM_PATH = "/api/1/item/{item_id}"
    GET_SELLER_ITEMS_PATH = "/api/1/{seller_id}/item"
    GET_STATISTICS_PATH = "/api/1/statistic/{item_id}"

    def __init__(self, base_url: str | None = None, timeout: int | None = None) -> None:
        self.base_url = (base_url or settings.base_url).rstrip("/")
        self.timeout = timeout or settings.request_timeout
        self.session = requests.Session()

    def create_item(self, payload: dict[str, Any]) -> Response:
        return self._request("POST", self.CREATE_ITEM_PATH, json_body=payload)

    def create_item_with_raw_body(
        self,
        raw_body: str,
        headers: dict[str, str] | None = None,
    ) -> Response:
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)
        return self._request("POST", self.CREATE_ITEM_PATH, data=raw_body, headers=request_headers)

    def get_item(self, item_id: str) -> Response:
        return self._request("GET", self.GET_ITEM_PATH.format(item_id=item_id))

    def get_seller_items(self, seller_id: int | str) -> Response:
        return self._request("GET", self.GET_SELLER_ITEMS_PATH.format(seller_id=seller_id))

    def get_statistics(self, item_id: str) -> Response:
        return self._request("GET", self.GET_STATISTICS_PATH.format(item_id=item_id))

    def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        data: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        url = f"{self.base_url}{path}"
        with allure.step(f"{method} {path}"):
            self._attach_request(
                method=method,
                url=url,
                json_body=json_body,
                data=data,
                headers=headers,
            )
            response = self.session.request(
                method=method,
                url=url,
                json=json_body,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
            self._attach_response(response)
            return response

    @staticmethod
    def _attach_request(
        *,
        method: str,
        url: str,
        json_body: dict[str, Any] | None,
        data: str | None,
        headers: dict[str, str] | None,
    ) -> None:
        request_meta = {
            "method": method,
            "url": url,
            "headers": headers or {},
        }
        allure.attach(
            json.dumps(request_meta, ensure_ascii=False, indent=2),
            name="request-meta",
            attachment_type=allure.attachment_type.JSON,
        )
        if json_body is not None:
            allure.attach(
                json.dumps(json_body, ensure_ascii=False, indent=2),
                name="request-json",
                attachment_type=allure.attachment_type.JSON,
            )
        if data is not None:
            allure.attach(
                data,
                name="request-raw-body",
                attachment_type=allure.attachment_type.TEXT,
            )

    @staticmethod
    def _attach_response(response: Response) -> None:
        allure.attach(
            json.dumps(
                {"status_code": response.status_code, "headers": dict(response.headers)},
                ensure_ascii=False,
                indent=2,
            ),
            name="response-meta",
            attachment_type=allure.attachment_type.JSON,
        )
        try:
            body = json.dumps(response.json(), ensure_ascii=False, indent=2)
            attachment_type = allure.attachment_type.JSON
        except ValueError:
            body = response.text
            attachment_type = allure.attachment_type.TEXT
        allure.attach(body, name="response-body", attachment_type=attachment_type)