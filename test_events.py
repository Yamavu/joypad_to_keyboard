import pytest
from unittest.mock import MagicMock, patch
from evdev import ecodes

from config.sn30 import (
    BTN_MAPPING,
    ABS_HAT_MAPPING,
    INITIAL_HAT_VALUE,
    DEVICE_NAME,
    VENDOR_ID,
    PRODUCT_ID,
)
from mapper import Mapper

# Assuming this is the function you are testing
def trigger_volume_up(ui_device):
    ui_device.write(ecodes.EV_KEY, ecodes.KEY_VOLUMEUP, 1)
    ui_device.write(ecodes.EV_KEY, ecodes.KEY_VOLUMEUP, 0)
    ui_device.syn()


@pytest.fixture
def mapper():
    mock_device = MagicMock()
    return Mapper(mock_device, BTN_MAPPING, ABS_HAT_MAPPING, INITIAL_HAT_VALUE)

def test_syn(mapper):
    mapper.send_keystroke(ecodes.BTN_X, 1, True)
    assert mapper.output_device.mock_calls
    assert mapper.output_device.syn.called

def test_keystrokes(mapper):
    btn = ecodes.BTN_TL
    value = 1
    mapper.send_keystroke(btn, value, True)
    calls = mapper.output_device.write.call_args_list
    args = [call.args for call in calls] 
    print(args)
    wanted = [(1, args, value) for args in BTN_MAPPING[btn]]
    print(wanted)
    assert args == wanted

def test_keystrokes_release(mapper):
    btn = ecodes.BTN_TL
    value = 0
    mapper.send_keystroke(btn, value, False)
    calls = mapper.output_device.write.call_args_list
    args = [call.args for call in calls] 
    print(args)
    wanted = [(1, args, value) for args in BTN_MAPPING[btn]]
    wanted.reverse()
    print(wanted)
    assert args == wanted