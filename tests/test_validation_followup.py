# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
from pathlib import Path


CONNECTOR = Path(__file__).parents[1] / "microsoftintune_connector.py"
SOURCE = CONNECTOR.read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)


def _function_source(name: str) -> str:
    node = next(item for item in ast.walk(TREE) if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == name)
    return ast.get_source_segment(SOURCE, node) or ""


def test_login_redirect_validates_nonce_before_reading_sensitive_url():
    source = _function_source("_handle_login_redirect")
    compare_position = source.index("hmac.compare_digest")
    url_position = source.index("url = state.get(key)")

    assert 'request.GET.get("state_nonce"' in source
    assert compare_position < url_position


def test_displayed_oauth_start_link_carries_pending_nonce():
    source = _function_source("_handle_test_connectivity")

    assert 'urlparse.urlencode({"asset_id": self._asset_id, "state_nonce": flow_nonce})' in source
    assert 'f"{app_rest_url}/start_oauth?{start_query}"' in source
