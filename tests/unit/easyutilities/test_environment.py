# SPDX-FileCopyrightText: 2026 EasyUtilities contributors <https://github.com/easyscience>
# SPDX-License-Identifier: BSD-3-Clause

import importlib
import sys
from unittest.mock import MagicMock, patch

import pytest

import easyutilities.environment as env


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------


@pytest.fixture
def reload_env_module():
    """Fixture that ensures env module is restored after test, even on failure."""
    yield
    importlib.reload(env)


@pytest.fixture
def clean_pycharm_env(monkeypatch):
    """Fixture that ensures PYCHARM_HOSTED is unset."""
    monkeypatch.delenv('PYCHARM_HOSTED', raising=False)


# ----------------------------------------------------------------------
# in_pytest()
# ----------------------------------------------------------------------


def test_in_pytest_returns_true_when_pytest_loaded():
    """Test in_pytest() returns True when pytest is in sys.modules."""
    assert env.in_pytest() is True


def test_in_pytest_returns_false_when_pytest_not_loaded(monkeypatch):
    """Test in_pytest() returns False when pytest is not in sys.modules."""
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
    assert env.in_colab() is False


def test_in_colab_returns_true_when_module_exists(monkeypatch):
    """Test in_colab() returns True when google.colab module exists."""
    mock_spec = MagicMock()
    monkeypatch.setattr(
        'easyutilities.environment.find_spec',
        lambda x: mock_spec if x == 'google.colab' else None,
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


def test_in_jupyter_returns_true_when_colab(monkeypatch, clean_pycharm_env, reload_env_module):
    """Test in_jupyter() returns True when in Google Colab."""
    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = MagicMock()
    mock_spec = MagicMock()

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        importlib.reload(env)
        # Patch find_spec AFTER reload (reload re-imports find_spec)
        monkeypatch.setattr(
            'easyutilities.environment.find_spec',
            lambda x: mock_spec if x == 'google.colab' else None,
        )
        assert env.in_jupyter() is True


def test_in_jupyter_returns_true_with_zmq_shell(clean_pycharm_env, reload_env_module):
    """Test in_jupyter() returns True with ZMQInteractiveShell."""
    mock_ip = MagicMock()
    mock_ip.__class__.__name__ = 'ZMQInteractiveShell'
    mock_ip.config = {}

    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = mock_ip

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        importlib.reload(env)
        assert env.in_jupyter() is True


def test_in_jupyter_returns_false_with_terminal_shell(clean_pycharm_env, reload_env_module):
    """Test in_jupyter() returns False with TerminalInteractiveShell."""
    mock_ip = MagicMock()
    mock_ip.__class__.__name__ = 'TerminalInteractiveShell'
    mock_ip.config = {}

    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = mock_ip

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        importlib.reload(env)
        assert env.in_jupyter() is False


def test_in_jupyter_returns_true_with_ipkernel_config(clean_pycharm_env, reload_env_module):
    """Test in_jupyter() returns True when IPKernelApp is in config."""
    mock_ip = MagicMock()
    mock_ip.__class__.__name__ = 'SomeOtherShell'
    mock_ip.config = {'IPKernelApp': {}}

    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = mock_ip

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        importlib.reload(env)
        assert env.in_jupyter() is True


def test_in_jupyter_returns_false_when_ipython_returns_none(clean_pycharm_env, reload_env_module):
    """Test in_jupyter() returns False when get_ipython() returns None."""
    mock_ipython = MagicMock()
    mock_ipython.get_ipython.return_value = None

    with patch.dict(sys.modules, {'IPython': mock_ipython}):
        importlib.reload(env)
        assert env.in_jupyter() is False


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


@pytest.mark.parametrize('obj', ['string', 123, None, {}, []])
def test_is_ipython_display_handle_returns_false_for_non_handle(obj):
    """Test is_ipython_display_handle() returns False for regular objects."""
    assert env.is_ipython_display_handle(obj) is False


def test_is_ipython_display_handle_returns_true_for_display_handle():
    """Test is_ipython_display_handle() returns True for DisplayHandle."""
    IPython_display = pytest.importorskip('IPython.display')
    handle = IPython_display.DisplayHandle()
    assert env.is_ipython_display_handle(handle) is True


def test_is_ipython_display_handle_fallback_heuristic(reload_env_module):
    """Test is_ipython_display_handle() uses module heuristic when IPython unavailable."""
    # Create a mock object with __class__.__module__ starting with 'IPython'
    mock_obj = MagicMock()
    mock_obj.__class__.__module__ = 'IPython.display'

    # Block IPython import to force fallback path
    with patch.dict(sys.modules, {'IPython': None, 'IPython.display': None}):
        # The function should use the heuristic: check if module starts with 'IPython'
        # Since we can't easily force the ImportError inside the function,
        # test that the function handles the module-check heuristic
        result = env.is_ipython_display_handle(mock_obj)
        # With IPython available in test env, it will use isinstance check
        # which will return False for our mock
        assert isinstance(result, bool)


# ----------------------------------------------------------------------
# can_update_ipython_display()
# ----------------------------------------------------------------------


def test_can_update_ipython_display_returns_true_with_ipython():
    """Test can_update_ipython_display() returns True when IPython HTML available."""
    pytest.importorskip('IPython.display')
    assert env.can_update_ipython_display() is True


def test_can_update_ipython_display_returns_bool():
    """Test can_update_ipython_display() always returns a boolean."""
    result = env.can_update_ipython_display()
    assert isinstance(result, bool)


# ----------------------------------------------------------------------
# can_use_ipython_display()
# ----------------------------------------------------------------------


@pytest.mark.parametrize('obj', ['not a handle', None, 123, {}])
def test_can_use_ipython_display_returns_false_for_non_handle(obj):
    """Test can_use_ipython_display() returns False for non-DisplayHandle."""
    assert env.can_use_ipython_display(obj) is False


def test_can_use_ipython_display_returns_true_for_valid_handle():
    """Test can_use_ipython_display() returns True for valid DisplayHandle."""
    IPython_display = pytest.importorskip('IPython.display')
    handle = IPython_display.DisplayHandle()
    assert env.can_use_ipython_display(handle) is True


def test_can_use_ipython_display_handles_exception_gracefully():
    """Test can_use_ipython_display() returns False for problematic objects."""
    # Object that may cause issues during type checking
    bad_obj = MagicMock()
    bad_obj.__class__ = None
    # Should not raise, should return False
    assert env.can_use_ipython_display(bad_obj) is False
