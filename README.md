# Confirmation Dialog Python

A customizable confirmation dialog with timeout functionality for Python applications using Tkinter. This package provides a simple way to create modal confirmation dialogs that automatically cancel if no response is provided within a specified time.

## Features

- Customizable message and title
- Countdown timer display
- Auto-cancel functionality after timeout
- Yes/No buttons (default) or custom buttons with callbacks
- Dark theme by default (customizable background)
- Escape key support for quick cancellation
- Modal dialog behavior
- Centered window positioning

## Installation

```bash
pip install git+https://github.com/marcosogsantos/confirmation_dialog_py.git
```

## Basic Usage

Here's a simple example of how to use the confirmation dialog:

```python
from confirmation_dialog import ConfirmationDialog

# Create a confirmation dialog
dialog = ConfirmationDialog(
    message="Do you want to proceed with the operation?",
    title="Confirm Action",
    background="#121212",  # Optional: customize background color
    timeout=15000  # Optional: set timeout in milliseconds (default: 15000)
)

# Show the dialog and get the result
result = dialog.show_up()

if result:
    print("User clicked Yes")
else:
    print("User clicked No or dialog timed out")
```

### Custom Buttons Example

You can also create a dialog with custom buttons and callbacks:

```python
from confirmation_dialog import ConfirmationDialog

def on_confirm():
    print("Confirm button clicked")

def on_reject():
    print("Reject button clicked")

def on_remember_later():
    print("Remember me later button clicked")

# Create a dialog with custom buttons
dialog = ConfirmationDialog(
    message="Would you like to save your preferences?",
    title="Save Preferences",
    custom_buttons=[
        ("Confirm", on_confirm),
        ("Reject", on_reject),
        ("Remember me later", on_remember_later)
    ]
)

# Show the dialog
dialog.show_up()

### Parameters

- `message` (str): The message to display in the dialog (default: "Do you want to continue?")
- `title` (str): The window title (default: "Confirmation")
- `background` (str): The background color in hex format (default: "#121212")
- `timeout` (int): Timeout duration in milliseconds before auto-cancel (default: 15000)
- `custom_buttons` (List[Tuple[str, Callable]]): Optional list of tuples containing (button_label, callback_function).
  If provided, these buttons will be shown instead of the default Yes/No buttons.

### Return Value

The `show_up()` method returns:
- `True` if the user clicks "Yes" (when using default buttons)
- `False` if the user clicks "No", presses Escape, or the dialog times out (when using default buttons)
- When using custom buttons, the return value is always `None` as the callbacks handle the actions

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## License

This project is licensed under the MIT License - see the LICENSE file for details.