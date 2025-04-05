# Confirmation Dialog Python

A customizable confirmation dialog with timeout functionality for Python applications using Tkinter. This package provides a simple way to create modal confirmation dialogs that automatically cancel if no response is provided within a specified time.

## Features

- Customizable message and title
- Countdown timer display
- Auto-cancel functionality after timeout
- Yes/No buttons
- Dark theme by default (customizable background)
- Escape key support for quick cancellation
- Modal dialog behavior
- Centered window positioning
- Optional state management support

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

### Parameters

- `message` (str): The message to display in the dialog (default: "Do you want to continue?")
- `title` (str): The window title (default: "Confirmation")
- `background` (str): The background color in hex format (default: "#121212")
- `timeout` (int): Timeout duration in milliseconds before auto-cancel (default: 15000)

### Return Value

The `show_up()` method returns:
- `True` if the user clicks "Yes"
- `False` if the user clicks "No", presses Escape, or the dialog times out

## Advanced Usage: State Management

For applications that need to track dialog state, you can implement the optional `StateManagerInterface`:

```python
from confirmation_dialog import ConfirmationDialog, StateManagerInterface

# Create a state manager that implements the StateManagerInterface
class MyStateManager(StateManagerInterface):
    def set(self, key: str, value: any) -> None:
        # Implement your state management logic here
        pass

# Create a confirmation dialog with state management
dialog = ConfirmationDialog(
    message="Do you want to proceed with the operation?",
    state_manager=MyStateManager()  # Optional: provide a state manager
)

result = dialog.show_up()
```

The state manager will track the last confirmation result under the key "last_confirmation".

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
