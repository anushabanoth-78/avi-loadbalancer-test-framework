import logging

logger = logging.getLogger(__name__)

def validate_response(response: dict, expected_keys: list) -> bool:
    if not response:
        return False
    return all(key in response for key in expected_keys)