"""
JSON schemas for validation, loaded from gitlab.com.
"""
import json
from .util import request_get_with_retry
from contextlib import contextmanager
from typing import Generator
import logging



@contextmanager
def _request_get_with_retry(url: str) -> Generator[dict, None, None]:
    logger = logging.getLogger(__name__)
    logger.debug('Loading JSON schema %s', url)

    with request_get_with_retry(url) as response:
        yield response.json()


with _request_get_with_retry('https://gitlab.com/huntsman-cancer-institute/risr/hea/hea-json-schemas/-/raw/master/wstlaction.json') as response_json:
    WSTL_ACTION_SCHEMA = response_json

with _request_get_with_retry('https://gitlab.com/huntsman-cancer-institute/risr/hea/hea-json-schemas/-/raw/master/wstl.json') as response_json:
    WSTL_SCHEMA = response_json

with _request_get_with_retry('https://gitlab.com/huntsman-cancer-institute/risr/hea/hea-json-schemas/-/raw/master/cjtemplate.json') as response_json:
    CJ_TEMPLATE_SCHEMA = response_json

with _request_get_with_retry('https://gitlab.com/huntsman-cancer-institute/risr/hea/hea-json-schemas/-/raw/master/nvpjson.json') as response_json:
    NVPJSON_SCHEMA = response_json
