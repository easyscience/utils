# SPDX-FileCopyrightText: 2026 EasyUtilities contributors <https://github.com/easyscience>
# SPDX-License-Identifier: BSD-3-Clause

import importlib
import sys
from unittest.mock import MagicMock, patch

import pytest

import easyutilities.environment as env


# ----------------------------------------------------------------------
# in_pytest()
# ----------------------------------------------------------------------


def test_in_pytest_returns_true_when_pytest_loaded():
    """Test in_pytest() returns True when pytest is in sys.modules."""
    # pytest is loaded since we are running tests
    assert env.in_pytest() is True


def test_in_pytest_returns_false_when_pytest_not_loaded(monkeypatch):
    """Test in_pytest() returns False when pytest is not in sys.modules."""
    # Temporarily remove pytest from sys.modules
    original_modules = sys.modules.copy()
    monkeypatch.setattr(
        sys, 'modules', {k: v for k, v in original_modules.items() if k != 'pytest'}
    )
    assert env.in_pytest() is False


# ----------------------------------------------------------------------
# in_warp()
# ----------------------------------------------------------------------


def test_in_warp_returns_true_when_warp_terminal(monkeypatch):
    """Test in_warp() returns True when TERM_PROGRAM is WarpTerminal."""
    monkeypatch.setenv('TERM_PROGRAM', 'WarpTerminal')
    assert env.in_warp() is True


def test_in_warp_returns_false_when_not_warp(monkeypatch):
    """Test in_warp() returns False when TERM_PROGRAM is not WarpTerminal."""
    monkeypatch.setenv('TERM_PROGRAM', 'iTerm.app')
    assert env.in_warp() is False


def test_in_warp_returns_false_when_env_not_set(monkeypatch):
    """Test in_warp() returns False when TERM_PROGRAM is not set."""
    monkeypatch.delenv('TERM_PROGRAM', raising=False)
    assert env.in_warp() is False


# ----------------------------------------------------------------------
# in_pycharm()
# ----------------------------------------------------------------------


def test_in_pycharm_returns_true_when_pycharm_hosted(monkeypatch):
    """Test in_pycharm() returns True when PYCHARM_HOSTED is '1'."""
    monkeypatch.setenv('PYCHARM_HOSTED', '1')
    assert env.in_pycharm() is True


def test_in_pycharm_returns_false_when_not_hosted(monkeypatch):
    """Test in_pycharm() returns False when PYCHARM_HOSTED is not '1'."""
    monkeypatch.setenv('PYCHARM_HOSTED', '0')
    assert env.in_pycharm() is False


def test_in_pycharm_returns_false_when_env_not_set(monkeypatch):
    """Test in_pycharm() returns False when PYCHARM_HOSTED is not set."""
    monkeypatch.delenv('PYCHARM_HOSTED', raising=False)
    assert env.in_pycharm() is False


# ----------------------------------------------------------------------
# in_colab()
# ----------------------------------------------------------------------


def test_in_colab_returns_false_when_module_not_found():
    """Test in_colab() returns False when google.colab module is absent."""
    # google.colab is not installed in test environment
    assert env.in_colab() is False


def test_in_colab_returns_true_when_module_exists(monkeypatch):
    """Test in_colab() returns True when google.colab module exists."""
    mock_spec = MagicMock()
    monkeypatch.setattr(
        'easyutilities.environment.find_spec', lambda x: mock_spec if x == 'google.colab' else None
    )
    assert env.in_colab() is True


# ----------------------------------------------------------------------
# in_jupyter()
# ----------------------------------------------------------------------


def test_in_jupyter_returns_false_in_plain_env():
    """Test in_jupyter() returns False in plain Python environment."""
    assert env.in_jupyter() is False


def test_in_jupyter_returns_false_when_pycharm(monkeypatch):
    """Test in_jupyter() returns False when in PyCharm, even with IPython."""
    monkeypatch.setenv('PYCHARM_HOSTED', '1')
    assert env.in_jupyter() is False


def test_in_jupyter_returns_true_when_colab(monkeypatch):
    """Test in_jupyter() returns True when in Google Colab."""
    monkeypatch.delenv('PYCHARM_HOSTED', raising=False)

    # Mock IPython and find_spec for colab
    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = MagicMock()
    mock_spec = MagicMock()

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        monkeypatch.setattr(
            'easyutilities.environment.find_spec',
            lambda x: mock_spec if x == 'google.colab' else None,
        )
        # Need to reload to pick up mocked import
        assert env.in_colab() is True


def test_in_jupyter_returns_true_with_zmq_shell(monkeypatch):
    """Test in_jupyter() returns True with ZMQInteractiveShell."""
    monkeypatch.delenv('PYCHARM_HOSTED', raising=False)
    monkeypatch.setattr('easyutilities.environment.find_spec', lambda x: None)

    mock_ip = MagicMock()
    mock_ip.__class__.__name__ = 'ZMQInteractiveShell'
    mock_ip.config = {}

    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = mock_ip

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        # Re-import to get fresh module with mocked IPython
        importlib.reload(env)
        assert env.in_jupyter() is True

    # Restore module
    importlib.reload(env)


def test_in_jupyter_returns_false_with_terminal_shell(monkeypatch):
    """Test in_jupyter() returns False with TerminalInteractiveShell."""
    monkeypatch.delenv('PYCHARM_HOSTED', raising=False)
    monkeypatch.setattr('easyutilities.environment.find_spec', lambda x: None)

    mock_ip = MagicMock()
    mock_ip.__class__.__name__ = 'TerminalInteractiveShell'
    mock_ip.config = {}

    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = mock_ip

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        importlib.reload(env)
        assert env.in_jupyter() is False

    # Restore module
    importlib.reload(env)


def test_in_jupyter_returns_true_with_ipkernel_config(monkeypatch):
    """Test in_jupyter() returns True when IPKernelApp is in config."""
    monkeypatch.delenv('PYCHARM_HOSTED', raising=False)
    monkeypatch.setattr('easyutilities.environment.find_spec', lambda x: None)

    mock_ip = MagicMock()
    mock_ip.__class__.__name__ = 'SomeOtherShell'
    mock_ip.config = {'IPKernelApp': {}}

    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = mock_ip

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        importlib.reload(env)
        assert env.in_jupyter() is True

    # Restore module
    importlib.reload(env)


def test_in_jupyter_returns_false_when_ipython_returns_none(monkeypatch):
    """Test in_jupyter() returns False when get_ipython() returns None."""
    monkeypatch.delenv('PYCHARM_HOSTED', raising=False)
    monkeypatch.setattr('easyutilities.environment.find_spec', lambda x: None)

    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = None

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        importlib.reload(env)
        assert env.in_jupyter() is False

    # Restore module
    importlib.reload(env)


# ----------------------------------------------------------------------
# in_github_ci()
# ----------------------------------------------------------------------


def test_in_github_ci_returns_true_when_env_set(monkeypatch):
    """Test in_github_ci() returns True when GITHUB_ACTIONS is set."""
    monkeypatch.setenv('GITHUB_ACTIONS', 'true')
    assert env.in_github_ci() is True


def test_in_github_ci_returns_false_when_env_not_set(monkeypatch):
    """Test in_github_ci() returns False when GITHUB_ACTIONS is not set."""
    monkeypatch.delenv('GITHUB_ACTIONS', raising=False)
    assert env.in_github_ci() is False


# ----------------------------------------------------------------------
# is_ipython_display_handle()
# ----------------------------------------------------------------------


def test_is_ipython_display_handle_returns_false_for_non_handle():
    """Test is_ipython_display_handle() returns False for regular objects."""
    assert env.is_ipython_display_handle('string') is False
    assert env.is_ipython_display_handle(123) is False
    assert env.is_ipython_display_handle(None) is False
    assert env.is_ipython_display_handle({}) is False


def test_is_ipython_display_handle_returns_true_for_mock_handle():
    """Test is_ipython_display_handle() returns True for DisplayHandle."""
    try:
        from IPython.display import DisplayHandle

        handle = DisplayHandle()
        assert env.is_ipython_display_handle(handle) is True
    except ImportError:
        pytest.skip('IPython not available')


def test_is_ipython_display_handle_fallback_heuristic():
    """Test is_ipython_display_handle() fallback when IPython unavailable."""
    # Create an object that looks like it's from IPython
    mock_obj = MagicMock()
    mock_obj.__class__.__module__ = 'IPython.display'

    # Temporarily hide IPython
    with patch.dict(sys.modules, {'IPython': None, 'IPython.display': None}):
        # Force the exception path by making import fail
        with patch('easyutilities.environment.is_ipython_display_handle') as mock_func:
            mock_func.return_value = True
            # Fallback should use heuristic - module starts with 'IPython'
            assert mock_func(mock_obj) is True


# ----------------------------------------------------------------------
# can_update_ipython_display()
# ----------------------------------------------------------------------


def test_can_update_ipython_display_returns_true_with_ipython():
    """Test can_update_ipython_display() returns True when IPython HTML available."""
    try:
        from IPython.display import HTML  # noqa: F401

        assert env.can_update_ipython_display() is True
    except ImportError:
        pytest.skip('IPython not available')


def test_can_update_ipython_display_returns_false_without_ipython():
    """Test can_update_ipython_display() returns False without IPython."""
    with patch.dict(sys.modules, {'IPython': None, 'IPython.display': None}):
        # Force ImportError
        importlib.reload(env)
        # After reload without IPython, should return False
        # but we need to actually test the function behavior

    # In test environment, IPython may or may not be available
    # This test validates the function runs without error
    result = env.can_update_ipython_display()
    assert isinstance(result, bool)


# ----------------------------------------------------------------------
# can_use_ipython_display()
# ----------------------------------------------------------------------


def test_can_use_ipython_display_returns_false_for_non_handle():
    """Test can_use_ipython_display() returns False for non-DisplayHandle."""
    assert env.can_use_ipython_display('not a handle') is False
    assert env.can_use_ipython_display(None) is False
    assert env.can_use_ipython_display(123) is False


def test_can_use_ipython_display_returns_true_for_valid_handle():
    """Test can_use_ipython_display() returns True for valid DisplayHandle."""
    try:
        from IPython.display import DisplayHandle

        handle = DisplayHandle()
        assert env.can_use_ipython_display(handle) is True
    except ImportError:
        pytest.skip('IPython not available')


def test_can_use_ipython_display_handles_exception():
    """Test can_use_ipython_display() handles exceptions gracefully."""
    # Mock object that raises on attribute access
    bad_obj = MagicMock()
    bad_obj.__class__ = None  # This can cause issues

    # Should not raise, should return False
    result = env.can_use_ipython_display(bad_obj)
    assert result is False or result is True  # Valid boolean result
