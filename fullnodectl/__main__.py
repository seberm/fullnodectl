import argparse
import logging
import os

from fullnodectl import (
    mod,
    errors,
    configurator,
)

log = logging.getLogger(__name__)


# DEFAULT_LOGGING_LEVEL = "DEBUG"
DEFAULT_LOGGING_LEVEL = "WARNING"


def main():
    parser = argparse.ArgumentParser(
        description="TODO",
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-l",
        "--log",
        action="store",
        type=str.upper,
        help="Logging level.",
        choices=["DEBUG", "WARNING", "INFO", "ERROR", "EXCEPTION"],
        default=DEFAULT_LOGGING_LEVEL,
    )

    parser.add_argument(
        "-c",
        "--config",
        action="store",
        help="Path to configuration file",

        # FIXME: Add possibility to load file from multiple locations
        default=os.path.join("fullnodectl.conf"),
    )

    module_subparsers = parser.add_subparsers(
        dest="module",
        help="Module name",
        required=True,
    )

    logging.basicConfig(level=DEFAULT_LOGGING_LEVEL)
    loaded_modules = mod.get_and_register_available_modules()

    for module in loaded_modules:
        module_parser = module_subparsers.add_parser(module.MODULE_NAME, help=module.MODULE_DESCRIPTION.split("\n", maxsplit=2)[1])
        mod.callback(module.MODULE_NAME, mod.HOOK_INIT_PARSERS, module_parser)

    args = parser.parse_args()

    # Setup the logging
    logging.basicConfig(level=args.log)

    # Load and validate the configuration file, set the defaults
    cnf = configurator.Config(args.config)

    try:
        return mod.callback(args.module, mod.HOOK_RUN, args, cnf.config)
    except errors.FullNodeCTLError as e:
        log.error(e)
        log.error("Program error, exiting.")
        return 99
