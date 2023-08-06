"""Simple module for showing GTK dialog"""

from typing import Union, Optional, Tuple

import gi  # type: ignore
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk  # type: ignore

TxtTuple = Tuple[Optional[str], bool]
TxtType = Union[TxtTuple, Optional[str]]


def show_msg(
        title: str,
        text: TxtType,
        sectext: TxtType = None,
        btns: Gtk.ButtonsType = Gtk.ButtonsType.OK,
        msgtype: Gtk.MessageType = Gtk.MessageType.INFO) -> None:
    """Opens GTK MessageDialog

    Args:
        title (str): Dialog caption
        text (TxtType): Dialog primary text, str or tuple: `(text, use_markup)`
        sectext (TxtType, optional): Dialog secondary text, str or tuple
        btns (Gtk.ButtonsType, optional): Dialog buttons
        msgtype (Gtk.MessageType, optional): Dialog message type
    """

    if isinstance(text, str) or text is None:
        txt: TxtTuple = (text, False)

    if isinstance(sectext, str) or sectext is None:
        sectxt: TxtTuple = (sectext, False)

    msg = Gtk.MessageDialog(
        title=title,
        text=txt[0],
        use_markup=txt[1],
        secondary_text=sectxt[0],
        secondary_use_markup=sectxt[1],
        buttons=btns,
        message_type=msgtype,
    )

    msg.connect(
        'response',
        lambda _a, _b: msg.destroy()
    )
    msg.connect('destroy', Gtk.main_quit)

    msg.show()
    Gtk.main()
