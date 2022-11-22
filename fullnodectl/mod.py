__license__ = "MIT"

import os
import sys
import re
import importlib
import logging
from glob import glob

from fullnodectl import errors

log = logging.getLogger(__name__)

_CUR_DIR = os.path.dirname(os.path.realpath(__file__))
_INTERNAL_MODS_DIR_PATH = os.path.join(_CUR_DIR, "modules")

# Hooks:
HOOK_INIT_PARSERS = "_init_parsers"
HOOK_INIT = "_init"
HOOK_RUN = "_run"

_REGISTERED_MODULES = {}


def _check_module_format(module):
    """
    All modules must have defined MODULE_HOOKS and MODULE_NAME. The MODULE_NAME must be in a correct format.
    """
    required_attrs = [
        "MODULE_NAME",
        "MODULE_HOOKS",
    ]

    for attr in required_attrs:
        if not hasattr(module, attr):
            log.error(f"Module {module.__file__} is missing required attribute: {attr}")
            return False

    if not re.match(r"^\w+([-]\w+)*$", module.MODULE_NAME):
        log.error(f"Module name is in a bad format: {module.MODULE_NAME}")
        return False

    return True


def load(filename):
    module_directory = os.path.dirname(os.path.realpath(filename))
    module_file, _ = os.path.splitext(filename)
    module_str = os.path.basename(module_file)

    # Add module directory into python path
    sys.path.insert(0, module_directory)
    log.debug(f"Adding {module_directory} into sys.path: {sys.path}")

    try:
        module = importlib.import_module(module_str)
    except ImportError:
        raise
    finally:
        log.debug("Removing first item (%s) from sys.path", sys.path[0])
        del sys.path[0]

    if not _check_module_format(module):
        raise ImportError(f"Module {filename} has a bad format.")

    log.info(f"Module '{module_str}' ({filename}) successfully loaded.")
    return module


def callback(module, hook, *argv, **kwargs):
    try:
        module_obj = _REGISTERED_MODULES[module]
    except KeyError:
        raise errors.FullNodeCTLError(f"Unknown module: {module}")

    try:
        log.debug(f"Calling '{hook}' callback of '{module_obj.__name__}' module. Args: %s", locals())
        module_obj.MODULE_HOOKS[hook](*argv, **kwargs)
    except KeyError:
        # Ignoring, the hook is not registered in the module
        pass


def callback_all(hook, *argv, **kwargs):
    for module in _REGISTERED_MODULES:
        callback(module.MODULE_NAME, hook, *argv, **kwargs)


def init(module_obj):
    if module_obj.MODULE_NAME in _REGISTERED_MODULES.keys():
        log.info(f"Module {module_obj.MODULE_NAME} already initialized! Skipping.")
    else:
        _REGISTERED_MODULES[module_obj.MODULE_NAME] = module_obj

    callback(module_obj.MODULE_NAME, HOOK_INIT)


def get_loaded_modules():
    return _REGISTERED_MODULES.values()


def get_and_register_available_modules():
    """
    Return list of internal modules which are available and *loadable*.
    """
    # Set of module files with removed __init__.py file
    module_files = {
        os.path.basename(f) for f in glob(os.path.join(_INTERNAL_MODS_DIR_PATH, "*.py"))
    } - set([
        "__init__.py",
    ])

    # Module tuples minus module name plus its options
    modules_to_register = [
        (m.split(".")[0], None, ) for m in module_files
    ]

    return register_internal_modules(modules_to_register)


def register_modules(modules):
    registered_modules = set()
    for m in modules:
        module_filename = m[0]
        module_opts = m[1] if len(m) == 2 else None

        try:
            module = load(module_filename)
        except ImportError as e:
            log.error(e)
            raise errors.FullNodeCTLError(
                f"Cannot load provided module {module_filename}, please check your input. Exiting."
            )

        # Register module hooks
        init(module)
        registered_modules.add(module)

    return registered_modules


def register_internal_modules(modules):
    mods_for_registration = set()
    for m in modules:
        module_name = m[0]
        module_opts = m[1] if len(m) == 2 else None
        mods_for_registration.add(
            (os.path.join(_INTERNAL_MODS_DIR_PATH, f"{module_name}.py"), module_opts,)
        )

    return register_modules(mods_for_registration)
