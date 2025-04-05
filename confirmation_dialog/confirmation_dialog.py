import tkinter as tk
from .state_manager_interface import StateManagerInterface

class ConfirmationDialog():
    def __init__(self, message="Do you want to continue?", title="Confirmation Dialog", background="#121212", timeout=15000, state_manager=None):
        """
        A custom confirmation dialog with a timeout that auto-cancels if no response is provided,
        and displays a countdown timer.
        
        :param message: Message to display.
        :param title: Title of the dialog window.
        :param background: Background color of the dialog.
        :param timeout: Timeout in milliseconds before auto-cancel.
        :param state_manager: An object implementing a state manager interface with a set(key, value) method.
        :raises TypeError: If state_manager is provided but doesn't implement the required interface.
        """
        if state_manager is not None and not isinstance(state_manager, StateManagerInterface):
            raise TypeError("State manager object must implement a set(key, value) method")
            
        self.state_manager = state_manager
        self.root = tk.Tk()
        self.root.configure(bg=background)
        self.root.title(title)
        self.root.attributes("-topmost", True)
        
        self.result = None
        self.timeout = timeout
        self.remaining = timeout // 1000  # countdown in seconds

        # Create the message label.
        self.message_label = tk.Label(self.root, text=message, font=("Arial", 14), fg="white", bg=background)
        self.message_label.pack(padx=20, pady=(10, 5))
        
        # Create a countdown label.
        self.countdown_label = tk.Label(self.root, text=f"Auto-cancel in {self.remaining} seconds", font=("Arial", 12), fg="white", bg=background)
        self.countdown_label.pack(pady=(0, 10))
        
        # Create a frame for buttons.
        btn_frame = tk.Frame(self.root, bg=background)
        btn_frame.pack(pady=10)
        
        # Define button styles
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 8,
            'relief': 'flat',
            'borderwidth': 0,
            'cursor': 'hand2'
        }
        
        # Yes button with neutral styling
        yes_button = tk.Button(
            btn_frame,
            text="Yes",
            command=self.on_yes,
            bg="#424242",  # Dark gray color
            fg="white",
            activebackground="#303030",  # Even darker gray on hover
            activeforeground="white",
            **button_style
        )
        yes_button.pack(side=tk.LEFT, padx=10)
        
        # No button with neutral styling
        no_button = tk.Button(
            btn_frame,
            text="No",
            command=self.on_no,
            bg="#424242",  # Same dark gray color
            fg="white",
            activebackground="#303030",  # Same darker gray on hover
            activeforeground="white",
            **button_style
        )
        no_button.pack(side=tk.LEFT, padx=10)
        
        # Add hover effects
        def on_enter(e, button, color):
            button['bg'] = color
        
        def on_leave(e, button, color):
            button['bg'] = color
        
        yes_button.bind("<Enter>", lambda e: on_enter(e, yes_button, "#303030"))
        yes_button.bind("<Leave>", lambda e: on_leave(e, yes_button, "#424242"))
        no_button.bind("<Enter>", lambda e: on_enter(e, no_button, "#303030"))
        no_button.bind("<Leave>", lambda e: on_leave(e, no_button, "#424242"))
        
        # Start updating the countdown.
        self.update_countdown()
        
        # Schedule auto-cancel after timeout.
        self.root.after(self.timeout, self.on_timeout)
        self.root.bind("<Escape>", lambda e: self.on_no())
        
        # Center the dialog relative to the parent.
        self.root.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (self.root.winfo_width() // 2)
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def update_countdown(self):
        """Update the countdown timer label every second."""
        if self.remaining > 0:
            self.countdown_label.config(text=f"Auto-cancel in {self.remaining} seconds")
            self.remaining -= 1
            self.root.after(1000, self.update_countdown)
        else:
            self.countdown_label.config(text="Auto-cancelling...")

    def on_yes(self):
        self.result = True
        if self.state_manager:
            self.state_manager.set("last_confirmation", True)
        self.root.destroy()

    def on_no(self):
        self.result = False
        if self.state_manager:
            self.state_manager.set("last_confirmation", False)
        self.root.destroy()

    def on_timeout(self):
        # Auto-cancel (close dialog without starting) if no response is provided.
        if self.result is None:
            self.result = False
            if self.state_manager:
                self.state_manager.set("last_confirmation", False)
            self.root.destroy()

    def show_up(self):
        """Starts the speed reader and returns True if finished normally, 
        or False if closed early. A confirmation dialog with a timeout countdown is shown first."""
        self.root.wait_window(self.root)
        return self.result 