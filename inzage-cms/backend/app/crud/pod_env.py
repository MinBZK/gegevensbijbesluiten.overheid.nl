import logging
import os

# Setup logger
logger = logging.getLogger(__name__)


async def get_all() -> list[dict[str, str]]:
    """
    Get environmental veriables of the pod
    """
    return [
        {name: value} for name, value in os.environ.items() if name in ("ENVIRONMENT", "URL_CONCEPT", "URL", "VERSION")
    ]
