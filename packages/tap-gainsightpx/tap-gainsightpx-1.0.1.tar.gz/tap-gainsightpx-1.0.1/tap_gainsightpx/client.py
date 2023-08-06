"""REST client handling, including GainsightPXStream base class."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class GainsightPXStream(RESTStream):
    """GainsightPX stream class."""

    current_record_count = 0

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="X-APTRINSIC-API-KEY",
            value=self.config["api_key"],
            location="header",
        )

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        res = response.json()
        scroll_id = res.get("scrollId")
        total_hits = res.get("totalHits")
        is_last_page = res.get("isLastPage")
        page_number = res.get("pageNumber")
        records_key = re.findall(r"\$\.(.*)\[\*\]", self.records_jsonpath)[0]

        if scroll_id is not None:
            self.current_record_count += len(res[records_key])
            if total_hits > self.current_record_count:
                next_page_token = scroll_id
            else:
                next_page_token = None
        else:
            if is_last_page:
                next_page_token = None
            else:
                next_page_token = page_number + 1

        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}

        page_size = self.config.get("page_size")
        if page_size:
            params["pageSize"] = page_size
        if self.replication_key:
            params["sort"] = self.replication_key

        return self.add_more_url_params(params, next_page_token)

    def add_more_url_params(
        self, params: dict, next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Add more params specific to the stream."""
        params["filter"] = ";".join(
            [
                f"date>={self.config['start_date']}",
                f"date<={self.config['end_date']}",
            ]
        )
        if next_page_token:
            params["scrollId"] = next_page_token
        return params
