import tkinter as tk
from typing import List, Tuple, Callable, Optional

class ConfirmationDialog():
    def __init__(
        self, 
        message="Do you want to continue?", 
        title="Confirmation Dialog", 
        background="#121212", 
        timeout=15000,
        custom_buttons: Optional[List[Tuple[str, Callable[[], None]]]] = None,
        monitor_index: int = 0
    ):
        """
        A custom confirmation dialog with a timeout that auto-cancels if no response is provided,
        and displays a countdown timer.
        
        :param message: Message to display.
        :param title: Title of the dialog window.
        :param background: Background color of the dialog.
        :param timeout: Timeout in milliseconds before auto-cancel.
        :param custom_buttons: Optional list of tuples containing (button_label, callback_function).
                              If provided, these buttons will be shown instead of the default Yes/No buttons.
        :param monitor_index: Index of the monitor to display the dialog on (0-based). Defaults to 0 (primary monitor).
        """
        self.root = tk.Tk()
        self.root.configure(bg=background)
        self.root.title(title)
        self.root.attributes("-topmost", True)
        
        # Remove default title bar
        self.root.overrideredirect(True)
        
        # Create custom title bar
        title_bar = tk.Frame(self.root, bg="#1a1a1a", relief='flat', bd=0)
        title_bar.pack(fill=tk.X, side=tk.TOP)
        
        # Title label
        title_label = tk.Label(
            title_bar,
            text=title,
            bg="#1a1a1a",
            fg="#b0b0b0",  # Softer white/gray
            font=("Arial", 10, "bold"),
            padx=10
        )
        title_label.pack(side=tk.LEFT)
        
        # Close button
        close_button = tk.Button(
            title_bar,
            text="×",
            bg="#1a1a1a",
            fg="#b0b0b0",  # Softer white/gray
            font=("Arial", 12, "bold"),
            relief='flat',
            bd=0,
            command=self.on_no,
            padx=10,
            cursor="hand2"
        )
        close_button.pack(side=tk.RIGHT)
        
        # Add hover effects for close button
        close_button.bind("<Enter>", lambda e: close_button.configure(bg="#e81123", fg="white"))
        close_button.bind("<Leave>", lambda e: close_button.configure(bg="#1a1a1a", fg="#b0b0b0"))
        
        # Make window draggable
        def start_move(event):
            self.x = event.x
            self.y = event.y

        def stop_move(event):
            self.x = None
            self.y = None

        def do_move(event):
            if self.x is not None and self.y is not None:
                deltax = event.x - self.x
                deltay = event.y - self.y
                x = self.root.winfo_x() + deltax
                y = self.root.winfo_y() + deltay
                self.root.geometry(f"+{x}+{y}")
        
        title_bar.bind('<Button-1>', start_move)
        title_bar.bind('<ButtonRelease-1>', stop_move)
        title_bar.bind('<B1-Motion>', do_move)
        
        title_label.bind('<Button-1>', start_move)
        title_label.bind('<ButtonRelease-1>', stop_move)
        title_label.bind('<B1-Motion>', do_move)
        
        self.x = None
        self.y = None
        
        self.result = None
        self.timeout = timeout
        self.remaining = timeout // 1000  # countdown in seconds

        # Create the message label.
        self.message_label = tk.Label(self.root, text=message, font=("Arial", 14), fg="#e0e0e0", bg=background)  # Softer white
        self.message_label.pack(padx=20, pady=(10, 5))
        
        # Create a countdown label.
        self.countdown_label = tk.Label(self.root, text=f"Auto-cancel in {self.remaining} seconds", font=("Arial", 12), fg="#b0b0b0", bg=background)  # Softer white/gray
        self.countdown_label.pack(pady=(0, 10))
        
        # Create a frame for buttons.
        btn_frame = tk.Frame(self.root, bg=background)
        btn_frame.pack(pady=10)
        
        # Define button styles
        button_style = {
            'font': ('Arial', 10, 'bold'),
            'relief': 'flat',
            'borderwidth': 0,
            'cursor': 'hand2',
            'padx': 15,  # Horizontal padding
            'pady': 8,   # Vertical padding
            'anchor': 'center'  # Center text in button
        }
        
        if custom_buttons:
            # Create custom buttons
            for label, callback in custom_buttons:
                button = tk.Button(
                    btn_frame,
                    text=label,
                    command=lambda cb=callback: self.on_custom_button(cb),
                    bg="#424242",  # Dark gray color
                    fg="#e0e0e0",  # Softer white
                    activebackground="#303030",  # Even darker gray on hover
                    activeforeground="#ffffff",  # Brighter white on hover
                    **button_style
                )
                button.pack(side=tk.LEFT, padx=10)
                
                # Add hover effects
                button.bind("<Enter>", lambda e, b=button: on_enter(e, b, "#303030"))
                button.bind("<Leave>", lambda e, b=button: on_leave(e, b, "#424242"))
        else:
            # Yes button with neutral styling
            yes_button = tk.Button(
                btn_frame,
                text="Yes",
                command=self.on_yes,
                bg="#424242",  # Dark gray color
                fg="#e0e0e0",  # Softer white
                activebackground="#303030",  # Even darker gray on hover
                activeforeground="#ffffff",  # Brighter white on hover
                **button_style
            )
            yes_button.pack(side=tk.LEFT, padx=10)
            
            # No button with neutral styling
            no_button = tk.Button(
                btn_frame,
                text="No",
                command=self.on_no,
                bg="#424242",  # Same dark gray color
                fg="#e0e0e0",  # Softer white
                activebackground="#303030",  # Same darker gray on hover
                activeforeground="#ffffff",  # Brighter white on hover
                **button_style
            )
            no_button.pack(side=tk.LEFT, padx=10)
            
            # Add hover effects
            yes_button.bind("<Enter>", lambda e: on_enter(e, yes_button, "#303030"))
            yes_button.bind("<Leave>", lambda e: on_leave(e, yes_button, "#424242"))
            no_button.bind("<Enter>", lambda e: on_enter(e, no_button, "#303030"))
            no_button.bind("<Leave>", lambda e: on_leave(e, no_button, "#424242"))
        
        # Add hover effects
        def on_enter(e, button, color):
            button['bg'] = color
            button['fg'] = "#ffffff"  # Brighter white on hover
        
        def on_leave(e, button, color):
            button['bg'] = color
            button['fg'] = "#e0e0e0"  # Softer white on leave
        
        # Start updating the countdown.
        self.update_countdown()
        
        # Schedule auto-cancel after timeout.
        self.root.after(self.timeout, self.on_timeout)
        self.root.bind("<Escape>", lambda e: self.on_no())
        
        # Center the dialog on the specified monitor
        self.center_on_monitor(monitor_index)

    def center_on_monitor(self, monitor_index: int = 0):
        """Center the window on the specified monitor."""
        # Get screen information
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Update window geometry
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Calculate position to center on screen
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # On multi-monitor setups, we need to adjust the position
        try:
            # Try to get the number of monitors and their positions
            from tkinter import Tk
            temp_root = Tk()
            temp_root.withdraw()  # Hide the temporary window
            
            # Get the number of monitors
            monitors = temp_root.tk.call('winfo', 'screen', '.')
            if monitors > 1:
                # Get the monitor dimensions
                monitor_width = screen_width // monitors
                # Adjust x position based on monitor index
                x = (monitor_width * monitor_index) + ((monitor_width - width) // 2)
            
            temp_root.destroy()
        except:
            # If anything fails, just center on the primary monitor
            pass
        
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
        self.root.destroy()

    def on_no(self):
        self.result = False
        self.root.destroy()

    def on_custom_button(self, callback):
        """Handle custom button click by executing the callback and closing the dialog."""
        callback()
        self.root.destroy()

    def on_timeout(self):
        # Auto-cancel (close dialog without starting) if no response is provided.
        if self.result is None:
            self.result = False
            self.root.destroy()

    def show_up(self):
        """Starts the speed reader and returns True if finished normally, 
        or False if closed early. A confirmation dialog with a timeout countdown is shown first."""
        self.root.wait_window(self.root)
        return self.result 