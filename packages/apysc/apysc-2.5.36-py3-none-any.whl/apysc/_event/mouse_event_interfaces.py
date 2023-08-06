"""Class implementation for the inheritance of each mouse
event interface.
"""

from apysc._event.click_mixin import ClickMixIn
from apysc._event.double_click_interface import DoubleClickInterface
from apysc._event.mouse_down_interface import MouseDownInterface
from apysc._event.mouse_move_interface import MouseMoveInterface
from apysc._event.mouse_out_interface import MouseOutInterface
from apysc._event.mouse_over_interface import MouseOverInterface
from apysc._event.mouse_up_mixin import MouseUpMixIn


class MouseEventInterfaces(
    ClickMixIn,
    DoubleClickInterface,
    MouseDownInterface,
    MouseUpMixIn,
    MouseOverInterface,
    MouseOutInterface,
    MouseMoveInterface,
):
    """Class implementation for the inheritance of each mouse
    event mix-ins.
    """
