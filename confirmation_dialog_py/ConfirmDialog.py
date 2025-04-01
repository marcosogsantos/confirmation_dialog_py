import tkinter as tk

class ConfirmDialog():
    def __init__(self, message="Do you want to continue?", title="Confirmation", background="#121212", timeout=15000):
        """
        A custom confirmation dialog with a timeout that auto-cancels if no response is provided,
        and displays a countdown timer.
        
        :param parent: Parent window.
        :param message: Message to display.
        :param timeout: Timeout in milliseconds before auto-cancel.
        """
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
        
        # Yes and No buttons.
        yes_button = tk.Button(btn_frame, text="Yes", command=self.on_yes, font=("Arial", 12))
        yes_button.pack(side=tk.LEFT, padx=5)
        no_button = tk.Button(btn_frame, text="No", command=self.on_no, font=("Arial", 12))
        no_button.pack(side=tk.LEFT, padx=5)
        
        # Make this window modal.
        # self.root.transient(self.root)
        # self.root.grab_set()
        
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
        self.root.destroy()

    def on_no(self):
        self.result = False
        self.root.destroy()

    def on_timeout(self):
        # Auto-cancel (close dialog without starting) if no response is provided.
        if self.result is None:
            self.result = False
            self.root.destroy()


    def start(self):
        """Starts the speed reader and returns True if finished normally, 
        or False if closed early. A confirmation dialog with a timeout countdown is shown first."""
        self.root.wait_window(self.root)
        # self.root.mainloop()
        return self.result