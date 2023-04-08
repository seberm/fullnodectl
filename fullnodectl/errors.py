__license__ = "MIT"

import logging


log = logging.getLogger(__name__)


# Main exception handler
class FullNodeCTLError(Exception):
    ...
