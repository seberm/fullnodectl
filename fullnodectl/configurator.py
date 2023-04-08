import os
import logging

from configobj import (
    ConfigObj,
    validate,
)

log = logging.getLogger(__name__)


class Config:
    # FIXME: Validator is not working correctly
    SPEC = """
        [bitcoin]
        # FIXME: only one of them can be defined
        config_file = string
        url = string

        [electrum]
        url = string

        [mempool]
        api_url = string

        [node]
        service_bitcoind = string(default='bitcoind')
        service_ln = option('lnd', 'clightning', default='lnd')
        service_electrum = option('electrs', 'fulctrum', default='electrs')
    """

    def __init__(self, filename):
        self.filename = filename
        self._init_config_parser()

    def _init_config_parser(self):
        if not os.path.isfile(self.filename):
            log.warning("Configuration file does not exist! Trying to use defaults.")

        self.config = ConfigObj(
            infile=self.filename,
            configspec=self.SPEC.split("\n"),
        )
        self.config.validate(validate.Validator(), copy=True)
