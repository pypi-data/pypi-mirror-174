# showdialog
Simple module for showing GTK dialog.

## Install
```bash
pip install showdialog
```

## Usage

### showdialog.show_msg(title, text, sectext, btns, msgtype)
Opens GTK MessageDialog

#### Args
|Name|Type|Description|Default value|
|:--:|:--:|:----------|:------:|
|title|`str`|Dialog caption|*Required*|
|text|`Tuple[Optional[str], bool] | Optional[str]`|Dialog primary text, str or tuple: `(text, use_markup)`|*Required*|
|sectext|`Tuple[Optional[str], bool] | Optional[str]`, optional|Dialog secondary text, str or tuple|`None`|
|btns|`Gtk.ButtonsType`|Dialog buttons|`Gtk.ButtonsType.OK`|
|msgtype|`Gtk.MessageType`|Dialog message type|`Gtk.MessageType.INFO`|

#### Example:
```python
from showdialog import show_msg
show_msg(title='', text='Hello world!')
```
