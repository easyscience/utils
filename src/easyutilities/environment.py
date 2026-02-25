# SPDX-FileCopyrightText: 2026 EasyUtilities contributors <https://github.com/easyscience>
# SPDX-License-Identifier: BSD-3-Clause
"""Runtime environment detection utilities.

This module provides functions to detect the current execution
environment, including testing frameworks, terminals, IDEs, notebook
environments, and CI systems. It also includes helpers for
IPython/Jupyter display handling.
"""

from __future__ import annotations

import os
import sys
from importlib.util import find_spec


# ----------------------------------------------------------------------
# Testing
# ----------------------------------------------------------------------


def in_pytest() -> bool:
    """Determine if the current environment is running under pytest.

    Returns:
        bool: True if pytest is loaded in sys.modules, False otherwise.
    """
    return 'pytest' in sys.modules


# ----------------------------------------------------------------------
# Terminal / IDE
# ----------------------------------------------------------------------


def in_warp() -> bool:
    """Determine if the current environment is Warp terminal.

    Returns:
        bool: True if running inside Warp terminal, False otherwise.
    """
    return os.getenv('TERM_PROGRAM') == 'WarpTerminal'


def in_pycharm() -> bool:
    """Determine if the current environment is PyCharm.

    Returns:
        bool: True if running inside PyCharm, False otherwise.
    """
    return os.environ.get('PYCHARM_HOSTED') == '1'


# ----------------------------------------------------------------------
# Notebook environments
# ----------------------------------------------------------------------


def in_colab() -> bool:
    """Determine if the current environment is Google Colab.

    Returns:
        bool: True if running in Google Colab, False otherwise.
    """
    try:
        return find_spec('google.colab') is not None
    except ModuleNotFoundError:  # pragma: no cover - importlib edge case
        return False


def in_jupyter() -> bool:
    """Determine if the current environment is a Jupyter Notebook.

    Uses multiple detection strategies including IPython availability,
    config-based detection, and shell class name inspection.

    Returns:
        bool: True if running inside a Jupyter Notebook, False otherwise.
    """
    try:
        import IPython  # type: ignore[import-not-found]
    except ImportError:  # pragma: no cover - optional dependency
        ipython_mod = None
    else:
        ipython_mod = IPython
    if ipython_mod is None:
        return False
    if in_pycharm():
        return False
    if in_colab():
        return True

    try:
        ip = ipython_mod.get_ipython()  # type: ignore[attr-defined]
        if ip is None:
            return False
        # Prefer config-based detection when available (works with
        # tests).
        has_cfg = hasattr(ip, 'config') and isinstance(ip.config, dict)
        if has_cfg and 'IPKernelApp' in ip.config:  # type: ignore[index]
            return True
        shell = ip.__class__.__name__
        if shell == 'ZMQInteractiveShell':  # Jupyter or qtconsole
            return True
        if shell == 'TerminalInteractiveShell':
            return False
        return False
    except Exception:
        return False


# ----------------------------------------------------------------------
# CI
# ----------------------------------------------------------------------


def in_github_ci() -> bool:
    """Determine if the current environment is GitHub Actions CI.

    Returns:
        bool: True if ``GITHUB_ACTIONS`` env var is set, False otherwise.
    """
    return os.environ.get('GITHUB_ACTIONS') is not None


# ----------------------------------------------------------------------
# IPython / Jupyter helpers
# ----------------------------------------------------------------------


def is_ipython_display_handle(obj: object) -> bool:
    """Check if an object is an IPython DisplayHandle instance.

    Tries to import ``IPython.display.DisplayHandle`` and uses
    ``isinstance`` when available. Falls back to a conservative
    module name heuristic if IPython is missing.

    Args:
        obj: The object to check.

    Returns:
        bool: True if ``obj`` is a DisplayHandle, False otherwise.
    """
    try:  # Fast path when IPython is available
        from IPython.display import DisplayHandle  # type: ignore[import-not-found]

        try:
            return isinstance(obj, DisplayHandle)
        except Exception:
            return False
    except Exception:
        # Fallback heuristic when IPython is unavailable
        try:
            mod = getattr(getattr(obj, '__class__', None), '__module__', '')
            return isinstance(mod, str) and mod.startswith('IPython')
        except Exception:
            return False


def can_update_ipython_display() -> bool:
    """Check if IPython HTML display utilities are available.

    This indicates we can safely construct ``IPython.display.HTML``
    and update a display handle.

    Returns:
        bool: True if IPython HTML display is available, False otherwise.
    """
    try:
        from IPython.display import HTML  # type: ignore[import-not-found]  # noqa: F401

        return True
    except Exception:
        return False


def can_use_ipython_display(handle: object) -> bool:
    """Check if a given IPython DisplayHandle can be updated.

    Combines type checking of the handle with availability of IPython
    HTML utilities.

    Args:
        handle: The display handle object to check.

    Returns:
        bool: True if the handle can be updated, False otherwise.
    """
    try:
        return is_ipython_display_handle(handle) and can_update_ipython_display()
    except Exception:
        return False
